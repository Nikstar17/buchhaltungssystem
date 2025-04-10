import ApiService from './api.service';
import UserChartOfAccountSettingsService from './user-chart-of-account-settings.service';

/**
 * Service zur Verwaltung von Kontenrahmen
 */
class ChartOfAccountsService {
  /**
   * Alle Kontenrahmen abrufen
   * @returns {Promise<Array>} Liste der Kontenrahmen
   */
  static async getAll() {
    try {
      return await ApiService.get('/api/chart-of-accounts');
    } catch (error) {
      console.error('Fehler beim Abrufen der Kontenrahmen:', error);
      throw error;
    }
  }

  /**
   * Details eines einzelnen Kontenrahmens abrufen
   * @param {string} id - ID des Kontenrahmens
   * @returns {Promise<Object>} Kontenrahmendetails
   */
  static async getById(id) {
    try {
      return await ApiService.get(`/api/chart-of-accounts/${id}`);
    } catch (error) {
      console.error(`Fehler beim Abrufen des Kontenrahmens ${id}:`, error);
      throw error;
    }
  }

  /**
   * Alle Konten eines Kontenrahmens abrufen
   * @param {string} chartId - ID des Kontenrahmens
   * @returns {Promise<Array>} Liste der Konten
   */
  static async getAccounts(chartId) {
    try {
      return await ApiService.get(`/api/chart-of-accounts/${chartId}/accounts`);
    } catch (error) {
      console.error(`Fehler beim Abrufen der Konten für Kontenrahmen ${chartId}:`, error);
      throw error;
    }
  }

  /**
   * Neuen Kontenrahmen erstellen
   * @param {Object} chartData - Kontenrahmendaten
   * @returns {Promise<Object>} Erstellter Kontenrahmen
   */
  static async create(chartData) {
    try {
      return await ApiService.post('/api/chart-of-accounts', chartData);
    } catch (error) {
      console.error('Fehler beim Erstellen des Kontenrahmens:', error);
      throw error;
    }
  }

  /**
   * Kontenrahmen aktualisieren
   * @param {string} id - ID des Kontenrahmens
   * @param {Object} chartData - Aktualisierte Kontenrahmendaten
   * @returns {Promise<Object>} Aktualisierter Kontenrahmen
   */
  static async update(id, chartData) {
    try {
      return await ApiService.put(`/api/chart-of-accounts/${id}`, chartData);
    } catch (error) {
      console.error(`Fehler beim Aktualisieren des Kontenrahmens ${id}:`, error);
      throw error;
    }
  }
}

export default ChartOfAccountsService;
