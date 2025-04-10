import ApiService from './api.service';
import AuthService from './auth.service';
import DocumentService from './document.service';
import SupplierService from './supplier.service';
import TaxRateService from './tax-rate.service';
import JournalEntryService from './journal-entry.service';
import UtilsService from './utils.service';

// Exportiere alle Services zentral
export {
  ApiService,
  AuthService,
  DocumentService,
  SupplierService,
  TaxRateService,
  JournalEntryService,
  UtilsService,
};

// Default-Export für einfachen Import
export default {
  ApiService,
  AuthService,
  DocumentService,
  SupplierService,
  TaxRateService,
  JournalEntryService,
  UtilsService,
};
