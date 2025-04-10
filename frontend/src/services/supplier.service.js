import ApiService from './api.service';

/**
 * Service zur Verwaltung von Lieferanten
 */
class SupplierService {
  /**
   * Alle Lieferanten abrufen
   * @returns {Promise<Array>} Liste der Lieferanten
   */
  static async getSuppliers() {
    try {
      return await ApiService.get('/api/suppliers');
    } catch (error) {
      console.error('Fehler beim Abrufen der Lieferanten:', error);
      throw error;
    }
  }

  /**
   * Details eines einzelnen Lieferanten abrufen
   * @param {string} id - ID des Lieferanten
   * @returns {Promise<Object>} Lieferantendetails
   */
  static async getSupplierById(id) {
    try {
      return await ApiService.get(`/api/suppliers/${id}`);
    } catch (error) {
      console.error(`Fehler beim Abrufen des Lieferanten ${id}:`, error);
      throw error;
    }
  }

  /**
   * Neuen Lieferanten erstellen
   * @param {Object} supplierData - Lieferantendaten
   * @returns {Promise<Object>} Erstellter Lieferant
   */
  static async createSupplier(supplierData) {
    try {
      return await ApiService.post('/api/suppliers', supplierData);
    } catch (error) {
      console.error('Fehler beim Erstellen des Lieferanten:', error);
      throw error;
    }
  }

  /**
   * Lieferanten aktualisieren
   * @param {string} id - ID des Lieferanten
   * @param {Object} supplierData - Aktualisierte Lieferantendaten
   * @returns {Promise<Object>} Aktualisierter Lieferant
   */
  static async updateSupplier(id, supplierData) {
    try {
      return await ApiService.put(`/api/suppliers/${id}`, supplierData);
    } catch (error) {
      console.error(`Fehler beim Aktualisieren des Lieferanten ${id}:`, error);
      throw error;
    }
  }

  /**
   * Lieferanten löschen
   * @param {string} id - ID des zu löschenden Lieferanten
   * @returns {Promise<Object>} Antwortdaten
   */
  static async deleteSupplier(id) {
    try {
      return await ApiService.delete(`/api/suppliers/${id}`);
    } catch (error) {
      console.error(`Fehler beim Löschen des Lieferanten ${id}:`, error);
      throw error;
    }
  }

  /**
   * Lieferantenname anhand der ID abrufen
   * @param {Array} suppliers - Liste der Lieferanten
   * @param {string} supplierId - ID des Lieferanten
   * @returns {string} Name des Lieferanten oder 'Unbekannt'
   */
  static getSupplierName(suppliers, supplierId) {
    const supplier = suppliers.find((s) => s.id === supplierId);
    return supplier ? supplier.name : 'Unbekannt';
  }
}

export default SupplierService;
