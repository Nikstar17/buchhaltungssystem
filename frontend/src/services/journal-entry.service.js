import ApiService from './api.service';

/**
 * Service zur Verwaltung von Buchungseinträgen
 */
class JournalEntryService {
  /**
   * Alle Buchungseinträge abrufen
   * @returns {Promise<Array>} Liste der Buchungseinträge
   */
  static async getJournalEntries() {
    try {
      return await ApiService.get('/api/journal-entries');
    } catch (error) {
      console.error('Fehler beim Abrufen der Buchungseinträge:', error);
      throw error;
    }
  }

  /**
   * Details eines einzelnen Buchungseintrags abrufen
   * @param {string} id - ID des Buchungseintrags
   * @returns {Promise<Object>} Buchungseintragdetails
   */
  static async getJournalEntryById(id) {
    try {
      return await ApiService.get(`/api/journal-entries/${id}`);
    } catch (error) {
      console.error(`Fehler beim Abrufen des Buchungseintrags ${id}:`, error);
      throw error;
    }
  }

  /**
   * Neuen Buchungseintrag erstellen
   * @param {Object} journalEntryData - Buchungseintragsdaten
   * @returns {Promise<Object>} Erstellter Buchungseintrag
   */
  static async createJournalEntry(journalEntryData) {
    try {
      return await ApiService.post('/api/journal-entries', journalEntryData);
    } catch (error) {
      console.error('Fehler beim Erstellen des Buchungseintrags:', error);
      throw error;
    }
  }

  /**
   * Buchungseintrag aktualisieren
   * @param {string} id - ID des Buchungseintrags
   * @param {Object} journalEntryData - Aktualisierte Buchungseintragsdaten
   * @returns {Promise<Object>} Aktualisierter Buchungseintrag
   */
  static async updateJournalEntry(id, journalEntryData) {
    try {
      return await ApiService.put(`/api/journal-entries/${id}`, journalEntryData);
    } catch (error) {
      console.error(`Fehler beim Aktualisieren des Buchungseintrags ${id}:`, error);
      throw error;
    }
  }

  /**
   * Buchungseintrag löschen
   * @param {string} id - ID des zu löschenden Buchungseintrags
   * @returns {Promise<Object>} Antwortdaten
   */
  static async deleteJournalEntry(id) {
    try {
      return await ApiService.delete(`/api/journal-entries/${id}`);
    } catch (error) {
      console.error(`Fehler beim Löschen des Buchungseintrags ${id}:`, error);
      throw error;
    }
  }

  /**
   * Alle Buchungspositionen eines Buchungseintrags abrufen
   * @param {string} journalEntryId - ID des Buchungseintrags
   * @returns {Promise<Array>} Liste der Buchungspositionen
   */
  static async getJournalLines(journalEntryId) {
    try {
      return await ApiService.get(`/api/journal-entries/${journalEntryId}/lines`);
    } catch (error) {
      console.error(
        `Fehler beim Abrufen der Buchungspositionen für Buchungseintrag ${journalEntryId}:`,
        error
      );
      throw error;
    }
  }

  /**
   * Buchungen nach Periode filtern
   * @param {string} period - Periodenangabe (z.B. '2023-01')
   * @returns {Promise<Array>} Liste der Buchungseinträge im angegebenen Zeitraum
   */
  static async getJournalEntriesByPeriod(period) {
    try {
      return await ApiService.get(`/api/journal-entries?period=${period}`);
    } catch (error) {
      console.error(`Fehler beim Abrufen der Buchungseinträge für Periode ${period}:`, error);
      throw error;
    }
  }
}

export default JournalEntryService;
