import ApiService from './api.service';

/**
 * Service zur Verwaltung von Dokumenten/Belegen
 */
class DocumentService {
  /**
   * Alle Dokumente abrufen
   * @returns {Promise<Array>} Liste der Dokumente
   */
  static async getDocuments() {
    try {
      return await ApiService.get('/api/documents');
    } catch (error) {
      console.error('Fehler beim Abrufen der Dokumente:', error);
      throw error;
    }
  }

  /**
   * Nur offene Dokumente abrufen
   * @returns {Promise<Array>} Liste der offenen Dokumente
   */
  static async getOpenDocuments() {
    try {
      return await ApiService.get('/api/documents?status=OPEN');
    } catch (error) {
      console.error('Fehler beim Abrufen der offenen Dokumente:', error);
      throw error;
    }
  }

  /**
   * Details eines einzelnen Dokuments abrufen
   * @param {string} id - ID des Dokuments
   * @returns {Promise<Object>} Dokumentdetails
   */
  static async getDocumentById(id) {
    try {
      return await ApiService.get(`/api/documents/${id}`);
    } catch (error) {
      console.error(`Fehler beim Abrufen des Dokuments ${id}:`, error);
      throw error;
    }
  }

  /**
   * Line-Items eines Dokuments abrufen
   * @param {string} documentId - ID des Dokuments
   * @returns {Promise<Array>} Liste der Line-Items
   */
  static async getDocumentLineItems(documentId) {
    try {
      const response = await ApiService.get(`/api/documents/${documentId}/line_items`);
      return response.line_items || [];
    } catch (error) {
      console.error(`Fehler beim Abrufen der Line-Items für Dokument ${documentId}:`, error);
      throw error;
    }
  }

  /**
   * Dokument-Datei im Base64-Format abrufen
   * @param {string} documentId - ID des Dokuments
   * @returns {Promise<Object>} Dateiinformationen mit Base64-Inhalt
   */
  static async getDocumentFileBase64(documentId) {
    try {
      return await ApiService.get(`/api/uploads/base64/${documentId}`);
    } catch (error) {
      console.error(`Fehler beim Abrufen der Datei für Dokument ${documentId}:`, error);
      throw error;
    }
  }

  /**
   * Neues Dokument erstellen
   * @param {FormData} formData - FormData-Objekt mit Dokumentdaten und Datei
   * @returns {Promise<Object>} Erstelltes Dokument
   */
  static async createDocument(formData) {
    try {
      return await ApiService.post('/api/documents', formData);
    } catch (error) {
      console.error('Fehler beim Erstellen des Dokuments:', error);
      throw error;
    }
  }

  /**
   * Dokument aktualisieren
   * @param {string} id - ID des Dokuments
   * @param {Object} documentData - Aktualisierte Dokumentdaten
   * @returns {Promise<Object>} Aktualisiertes Dokument
   */
  static async updateDocument(id, documentData) {
    try {
      return await ApiService.put(`/api/documents/${id}`, documentData);
    } catch (error) {
      console.error(`Fehler beim Aktualisieren des Dokuments ${id}:`, error);
      throw error;
    }
  }

  /**
   * Dokument löschen
   * @param {string} id - ID des zu löschenden Dokuments
   * @returns {Promise<Object>} Antwortdaten
   */
  static async deleteDocument(id) {
    try {
      return await ApiService.delete(`/api/documents/${id}`);
    } catch (error) {
      console.error(`Fehler beim Löschen des Dokuments ${id}:`, error);
      throw error;
    }
  }
}

export default DocumentService;
