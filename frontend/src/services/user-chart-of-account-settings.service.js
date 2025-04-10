import ApiService from './api.service';

/**
 * Service zur Verwaltung von Benutzereinstellungen für Konten eines Kontenrahmens
 */
class UserChartOfAccountSettingsService {
  /**
   * Benutzereinstellungen für Konten eines Kontenrahmens abrufen
   * @param {string} chartId - ID des Kontenrahmens
   * @returns {Promise<Array>} Liste der benutzerdefinierten Kontoeinstellungen
   */
  static async getByChartId(chartId) {
    try {
      return await ApiService.get(`/api/user-chart-of-account-settings/${chartId}`);
    } catch (error) {
      console.error(
        `Fehler beim Abrufen der Kontoeinstellungen für Kontenrahmen ${chartId}:`,
        error
      );
      throw error;
    }
  }

  /**
   * Benutzereinstellung für ein einzelnes Konto abrufen
   * @param {string} accountId - ID des Kontos
   * @returns {Promise<Object>} Benutzereinstellung für das Konto
   */
  static async getByAccountId(accountId) {
    try {
      return await ApiService.get(`/api/user-chart-of-account-settings/account/${accountId}`);
    } catch (error) {
      console.error(`Fehler beim Abrufen der Kontoeinstellung für Konto ${accountId}:`, error);
      throw error;
    }
  }

  /**
   * Benutzereinstellung für ein Konto aktualisieren
   * @param {string} accountId - ID des Kontos
   * @param {Object} settingsData - Aktualisierte Einstellungsdaten
   * @returns {Promise<Object>} Aktualisierte Benutzereinstellung
   */
  static async update(accountId, settingsData) {
    try {
      return await ApiService.put(
        `/api/user-chart-of-account-settings/account/${accountId}`,
        settingsData
      );
    } catch (error) {
      console.error(
        `Fehler beim Aktualisieren der Kontoeinstellung für Konto ${accountId}:`,
        error
      );
      throw error;
    }
  }

  /**
   * Mehrere Kontoeinstellungen gleichzeitig aktualisieren
   * @param {Array} settingsArray - Array mit Kontoeinstellungen
   * @returns {Promise<Object>} API-Antwort
   */
  static async updateBulk(settingsArray) {
    try {
      return await ApiService.put('/api/user-chart-of-account-settings/bulk', settingsArray);
    } catch (error) {
      console.error('Fehler beim Aktualisieren mehrerer Kontoeinstellungen:', error);
      throw error;
    }
  }

  /**
   * Konto als Favorit markieren oder Favorit entfernen
   * @param {string} accountId - ID des Kontos
   * @param {boolean} isFavorite - Status des Favoriten
   * @returns {Promise<Object>} Aktualisierte Benutzereinstellung
   */
  static async toggleFavorite(accountId, isFavorite) {
    try {
      return await ApiService.put(
        `/api/user-chart-of-account-settings/account/${accountId}/favorite`,
        {
          favorite: isFavorite,
        }
      );
    } catch (error) {
      console.error(`Fehler beim Ändern des Favoritenstatus für Konto ${accountId}:`, error);
      throw error;
    }
  }
}

export default UserChartOfAccountSettingsService;
