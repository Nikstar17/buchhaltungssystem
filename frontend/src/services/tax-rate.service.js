import ApiService from './api.service';

/**
 * Service zur Verwaltung von Steuersätzen
 */
class TaxRateService {
  /**
   * Alle Steuersätze abrufen
   * @returns {Promise<Array>} Liste der Steuersätze
   */
  static async getTaxRates() {
    try {
      return await ApiService.get('/api/tax_rates');
    } catch (error) {
      console.error('Fehler beim Abrufen der Steuersätze:', error);
      throw error;
    }
  }

  /**
   * Details eines einzelnen Steuersatzes abrufen
   * @param {string} id - ID des Steuersatzes
   * @returns {Promise<Object>} Steuersatzdetails
   */
  static async getTaxRateById(id) {
    try {
      return await ApiService.get(`/api/tax_rates/${id}`);
    } catch (error) {
      console.error(`Fehler beim Abrufen des Steuersatzes ${id}:`, error);
      throw error;
    }
  }

  /**
   * Neuen Steuersatz erstellen
   * @param {Object} taxRateData - Steuersatzdaten
   * @returns {Promise<Object>} Erstellter Steuersatz
   */
  static async createTaxRate(taxRateData) {
    try {
      return await ApiService.post('/api/tax_rates', taxRateData);
    } catch (error) {
      console.error('Fehler beim Erstellen des Steuersatzes:', error);
      throw error;
    }
  }

  /**
   * Steuersatz aktualisieren
   * @param {string} id - ID des Steuersatzes
   * @param {Object} taxRateData - Aktualisierte Steuersatzdaten
   * @returns {Promise<Object>} Aktualisierter Steuersatz
   */
  static async updateTaxRate(id, taxRateData) {
    try {
      return await ApiService.put(`/api/tax_rates/${id}`, taxRateData);
    } catch (error) {
      console.error(`Fehler beim Aktualisieren des Steuersatzes ${id}:`, error);
      throw error;
    }
  }

  /**
   * Steuersatz löschen
   * @param {string} id - ID des zu löschenden Steuersatzes
   * @returns {Promise<Object>} Antwortdaten
   */
  static async deleteTaxRate(id) {
    try {
      return await ApiService.delete(`/api/tax_rates/${id}`);
    } catch (error) {
      console.error(`Fehler beim Löschen des Steuersatzes ${id}:`, error);
      throw error;
    }
  }

  /**
   * Steuersatzprozent anhand der ID abrufen
   * @param {Array} taxRates - Liste der Steuersätze
   * @param {string} taxRateId - ID des Steuersatzes
   * @returns {string} Prozentsatz des Steuersatzes oder 'Unbekannt'
   */
  static getTaxRatePercentage(taxRates, taxRateId) {
    const taxRate = taxRates.find((rate) => rate.id === taxRateId);
    return taxRate ? taxRate.percentage : 'Unbekannt';
  }
}

export default TaxRateService;
