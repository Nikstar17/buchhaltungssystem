import json
import os
import sys
import uuid
from datetime import datetime
from flask import Flask
from sqlalchemy.exc import SQLAlchemyError

# Den Pfad zum Backend-Verzeichnis hinzufügen, um die Module korrekt zu importieren
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import db
from models.chart_of_accounts import ChartOfAccounts
from models.account import Account
from models.account_hierarchy import AccountHierarchy
from models.account_explanation import AccountExplanation
from models.enum import account_type_enum

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

def import_skr03():
    """
    Importiert den SKR03-Kontenrahmen aus der JSON-Datei in die Datenbank.
    """
    with app.app_context():
        # Prüfen, ob der SKR03 bereits existiert
        existing_skr03 = ChartOfAccounts.query.filter_by(name="SKR03").first()
        if existing_skr03:
            print("SKR03 existiert bereits in der Datenbank.")
            return

        # Neuen Kontenrahmen SKR03 erstellen
        skr03 = ChartOfAccounts(
            id=uuid.uuid4(),
            name="SKR03",
            description="Standardkontenrahmen 03 - Für Klein- und Mittelunternehmen",
            is_standard=True
        )

        try:
            db.session.add(skr03)
            db.session.commit()
            print(f"Kontenrahmen SKR03 erstellt mit ID: {skr03.id}")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Fehler beim Erstellen des Kontenrahmens: {str(e)}")
            return

        # SKR03 JSON-Datei einlesen
        skr03_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                      "Kontorahmen und Taxonomie", "skr03.json")

        try:
            with open(skr03_file_path, 'r', encoding='utf-8') as file:
                skr03_data = json.load(file)
        except Exception as e:
            print(f"Fehler beim Einlesen der SKR03 JSON-Datei: {str(e)}")
            return

        # Konten aus der JSON-Datei importieren
        for index, account_data in enumerate(skr03_data):
            if 'konto' not in account_data:
                continue

            konto = account_data.get('konto', {})
            # Im SKR03 ist die Nummer möglicherweise nicht direkt verfügbar
            # Wir nutzen den Index, falls keine Nummer vorhanden ist
            nummer = konto.get('nummer', str(index + 1))
            bezeichnung = konto.get('bezeichnung', '')

            if not bezeichnung:
                continue

            # Kontotyp bestimmen basierend auf der Kontonummer oder der Position im Kontenrahmen
            konto_typ = determine_account_type(nummer)

            # Hierarchie-Informationen extrahieren
            hierarchy_data = account_data.get('hierarchie', {})
            kontenklasse = hierarchy_data.get('kontenklasse', {})
            kontengruppe = hierarchy_data.get('kontengruppe', {})
            kontenart = hierarchy_data.get('kontenart', {})

            # Taxonomie-Informationen extrahieren
            taxonomie_data = account_data.get('taxonomie', {})

            # Konto erstellen
            account = Account(
                id=uuid.uuid4(),
                chart_of_accounts_id=skr03.id,
                number=nummer,
                name=bezeichnung,
                type=konto_typ,
                active=True,
                description=get_description(account_data),
                related_accounts=extract_related_accounts(account_data),
                account_class=kontenklasse.get('name', None),
                account_group=kontengruppe.get('name', None),
                account_type_custom=kontenart.get('name', None),
                taxonomy_element=taxonomie_data.get('hauptelement', None),
                taxonomy_type=taxonomie_data.get('type', None)
            )

            # Erläuterungen als separate Einträge in der account_explanations-Tabelle speichern
            erlaeuterungen = account_data.get('erlaeuterungen', [])
            for erlaeuterung in erlaeuterungen:
                # SKR03 könnte eine andere Struktur für Erläuterungen haben
                if isinstance(erlaeuterung, dict):
                    typ = erlaeuterung.get('typ', '')
                    text = erlaeuterung.get('text', '')
                else:
                    # Falls die Erläuterung direkt ein String ist
                    typ = 'info'
                    text = str(erlaeuterung)

                # Nur hinzufügen, wenn der Text nicht leer ist
                if text:
                    explanation = AccountExplanation(
                        id=uuid.uuid4(),
                        account_id=account.id,
                        type=typ,
                        text=text
                    )
                    account.explanations.append(explanation)

            # Hierarchie-Informationen als separate Einträge speichern
            if hierarchy_data:
                hierarchy = AccountHierarchy(
                    id=uuid.uuid4(),
                    account_id=account.id,
                    class_number=kontenklasse.get('nummer', ''),
                    class_name=kontenklasse.get('name', ''),
                    group_number=kontengruppe.get('nummer', ''),
                    group_name=kontengruppe.get('name', ''),
                    type_number=kontenart.get('nummer', ''),
                    type_name=kontenart.get('name', ''),
                    related_accounts=hierarchy_data.get('verwandte_konten', [])
                )

                account.hierarchy = hierarchy

            try:
                db.session.add(account)
            except SQLAlchemyError as e:
                print(f"Fehler beim Erstellen des Kontos {nummer}: {str(e)}")

            # Regelmäßiges Commit, um die Datenbank nicht zu überlasten
            if index % 100 == 0 and index > 0:
                try:
                    db.session.commit()
                    print(f"Konten bis Index {index} importiert.")
                except SQLAlchemyError as e:
                    db.session.rollback()
                    print(f"Fehler beim Commit der Konten: {str(e)}")

        # Finaler Commit
        try:
            db.session.commit()
            print("Import abgeschlossen!")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Fehler beim finalen Commit: {str(e)}")

def determine_account_type(account_number):
    """
    Bestimmt den Kontotyp basierend auf der Kontonummer gemäß der SKR03-Logik.
    """
    if not account_number or not account_number.isdigit():
        return "ASSET"

    num = int(account_number[0]) if account_number.isdigit() else 0

    if 0 <= num <= 2:
        return "ASSET"  # Aktivkonten
    elif 3 <= num <= 4:
        return "LIABILITY"  # Passivkonten
    elif num == 5:
        return "REVENUE"  # Ertragskonten
    elif 6 <= num <= 9:
        return "EXPENSE"  # Aufwandskonten
    else:
        return "ASSET"  # Standardmäßig Aktivkonto

def get_description(account_data):
    """
    Extrahiert die Bezeichnung des Kontos als Beschreibung.
    """
    konto = account_data.get('konto', {})
    return konto.get('bezeichnung', None)

def extract_related_accounts(account_data):
    """
    Extrahiert verwandte Konten aus den Hierarchiedaten.
    """
    hierarchie = account_data.get('hierarchie', {})
    verwandte_konten = hierarchie.get('verwandte_konten', [])
    return verwandte_konten if verwandte_konten else None

if __name__ == '__main__':
    import_skr03()