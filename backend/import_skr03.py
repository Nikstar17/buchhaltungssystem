#!/usr/bin/env python
import json
import logging
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("import_skr03")

# Add the current directory to the path so we can import our app modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Import app directly instead of using create_app
from app import app, db
from models.chart_of_accounts import ChartOfAccounts
from models.account import Account
from models.tax_rate import TaxRate


def import_skr03(json_file):
    """
    Import a SKR03 chart of accounts from a JSON file into the database.
    """
    # Ensure we have an absolute path
    json_file_path = (
        os.path.abspath(json_file) if not os.path.isabs(json_file) else json_file
    )

    if not os.path.exists(json_file_path):
        # If the path doesn't exist, try to find it relative to the script directory
        alternate_path = os.path.join(script_dir, os.path.basename(json_file))
        if os.path.exists(alternate_path):
            json_file_path = alternate_path
            logger.info(f"Using file at {json_file_path}")
        else:
            # Try to find it in the Kontorahmen und Taxonomie directory
            taxonomie_path = os.path.join(
                script_dir,
                "..",
                "Kontorahmen und Taxonomie",
                "skr03",
                os.path.basename(json_file),
            )
            if os.path.exists(taxonomie_path):
                json_file_path = taxonomie_path
                logger.info(f"Using file at {json_file_path}")
            else:
                logger.error(
                    f"File not found: {json_file_path} or {alternate_path} or {taxonomie_path}"
                )
                raise FileNotFoundError(
                    f"Could not find file {json_file} in current directory or script directory or taxonomie directory"
                )

    logger.info(f"Starting import of SKR03 chart of accounts from {json_file_path}")

    # Use the existing app context instead of creating a new one
    with app.app_context():
        try:
            # Check if SKR03 chart already exists
            existing_chart = ChartOfAccounts.query.filter_by(name="SKR03").first()
            if existing_chart:
                logger.warning(
                    f"A chart of accounts with name 'SKR03' already exists with ID: {existing_chart.id}"
                )
                proceed = input(
                    "Do you want to proceed with creating another one? (j/n): "
                )
                if proceed.lower() != "j":
                    logger.info("Import cancelled by user.")
                    return

            # Load the JSON file
            with open(json_file_path, "r", encoding="utf-8") as f:
                skr03_data = json.load(f)

            # Create the chart of accounts
            chart = ChartOfAccounts(
                id=str(uuid.uuid4()),
                name="SKR03",
                description="Standardkontenrahmen SKR03",
                is_standard=True,
                user_id=None,  # System chart
            )
            db.session.add(chart)
            db.session.commit()
            logger.info(f"Created new chart of accounts 'SKR03' with ID: {chart.id}")

            # Create/get tax rates
            tax_rates = {}
            # Get current date for valid_from field
            current_date = datetime.now().date()

            for rate_value in [0, 7, 19]:
                # Check if the tax rate already exists
                existing_rate = TaxRate.query.filter_by(percentage=rate_value).first()
                if existing_rate:
                    tax_rates[rate_value] = existing_rate
                    logger.info(
                        f"Using existing tax rate {rate_value}% with ID: {existing_rate.id}"
                    )
                else:
                    # Create a new tax rate
                    new_rate = TaxRate(
                        id=str(uuid.uuid4()),
                        name=f"{rate_value}% USt" if rate_value > 0 else "Steuerfrei",
                        percentage=rate_value,
                        valid_from=current_date,
                        active=True,
                        user_id=None,  # System tax rate
                    )
                    db.session.add(new_rate)
                    db.session.commit()
                    tax_rates[rate_value] = new_rate
                    logger.info(
                        f"Created new tax rate {rate_value}% with ID: {new_rate.id}"
                    )

            # Dictionary to temporarily store account objects by their IDs from the JSON file
            accounts_by_id = {}

            # First pass: Create all accounts without setting parent relationships
            for idx, account_data in enumerate(skr03_data["accounts"]):
                # Skip accounts that don't have necessary information or are empty
                if (
                    not account_data
                    or not account_data.get("id")
                    or not account_data.get("name", "")
                ):
                    continue

                # Map RECEIVABLE to ASSET and PAYABLE to LIABILITY if needed
                account_type = account_data.get("type", "NONE")
                if account_type == "RECEIVABLE":
                    account_type = "ASSET"
                elif account_type == "PAYABLE":
                    account_type = "LIABILITY"
                elif account_type == "BANK":
                    account_type = "ASSET"  # Behandle BANK-Konten als ASSET-Konten
                elif account_type not in [
                    "ASSET",
                    "LIABILITY",
                    "EQUITY",
                    "REVENUE",
                    "EXPENSE",
                    "INCOME",
                ]:
                    logger.warning(
                        f"Unknown account type: {account_type} for account {account_data.get('name')}, defaulting to ASSET"
                    )
                    account_type = "ASSET"

                # Map INCOME to REVENUE if needed
                if account_type == "INCOME":
                    account_type = "REVENUE"

                # Create the account
                account = Account(
                    id=str(uuid.uuid4()),
                    name=account_data.get("name", f"Account {idx}"),
                    number=account_data.get("code", str(idx)),
                    type=account_type,
                    chart_of_accounts_id=chart.id,
                    active=True,  # Set to active by default
                    level=None,  # This will be calculated later if needed
                )

                # Store the original ID for later linking
                original_id = account_data.get("id")
                accounts_by_id[original_id] = account

                # Try to find a tax rate if one is specified in the account data
                if "slots" in account_data and isinstance(account_data["slots"], list):
                    for slot in account_data["slots"]:
                        if slot.get("key") == "tax-rate" and slot.get("value"):
                            try:
                                rate_value = float(slot.get("value"))
                                if rate_value in tax_rates:
                                    # Check if the Account model has tax_rate_id attribute
                                    if hasattr(account, "tax_rate_id"):
                                        account.tax_rate_id = tax_rates[rate_value].id
                                        logger.debug(
                                            f"Assigned tax rate {rate_value}% to account {account.name}"
                                        )
                            except (ValueError, TypeError):
                                # If the tax rate value is not a valid number, skip it
                                pass

                # Set the XBRL mapping if available
                if "slots" in account_data and isinstance(account_data["slots"], list):
                    for slot in account_data["slots"]:
                        if slot.get("key") == "xbrl-element" and slot.get("value"):
                            # If the Account model has xbrl_element attribute
                            if hasattr(account, "xbrl_element"):
                                account.xbrl_element = slot.get("value")
                                logger.debug(
                                    f"Assigned XBRL element {slot.get('value')} to account {account.name}"
                                )

                db.session.add(account)

            # Commit all accounts first
            db.session.commit()
            logger.info(f"Created {len(accounts_by_id)} base accounts")

            # Second pass: Set up parent-child relationships based on category field
            categories = {}
            for account_data in skr03_data["accounts"]:
                if not account_data or not account_data.get("id"):
                    continue

                original_id = account_data.get("id")
                account = accounts_by_id.get(original_id)

                if account and "category" in account_data:
                    category_name = account_data["category"]

                    # Create category parent accounts if they don't exist
                    if category_name not in categories:
                        category_account = Account(
                            id=str(uuid.uuid4()),
                            name=category_name,
                            number=f"SKR03-{category_name}",
                            type=account.type,  # Use the same type as the child accounts
                            chart_of_accounts_id=chart.id,
                            active=True,
                            level=0,  # Top level category
                        )
                        db.session.add(category_account)
                        db.session.commit()
                        categories[category_name] = category_account
                        logger.info(f"Created category account: {category_name}")

                    # Set the parent relationship
                    account.parent_id = categories[category_name].id
                    account.level = 1  # Child level

            # Commit the parent-child relationships
            db.session.commit()
            logger.info(f"Updated account hierarchies")

            # Log success
            logger.info(
                f"Successfully imported SKR03 chart of accounts with {len(accounts_by_id)} accounts"
            )
            return chart.id

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during import: {str(e)}")
            raise


if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        # First look in the script directory
        default_file = os.path.join(script_dir, "skr03_full_xbrl_mapped.json")
        if os.path.exists(default_file):
            json_file = default_file
        else:
            # Also try the Kontorahmen directory
            kontorahmen_file = os.path.join(
                script_dir,
                "..",
                "Kontorahmen und Taxonomie",
                "skr03",
                "skr03_full_xbrl_mapped.json",
            )
            if os.path.exists(kontorahmen_file):
                json_file = kontorahmen_file
            else:
                # Default to just the filename and let the import_skr03 function handle the error
                json_file = "skr03_full_xbrl_mapped.json"
                logger.warning(
                    f"Using default filename. File will be searched in multiple locations."
                )

    try:
        chart_id = import_skr03(json_file)
        if chart_id:
            logger.info(f"Import completed successfully. Chart ID: {chart_id}")
        else:
            logger.info("Import was not completed.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(
            f"Please specify the correct path to the SKR03 JSON file as a command line argument."
        )
        logger.error(f"Import failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"Import failed: {str(e)}")
        sys.exit(1)
