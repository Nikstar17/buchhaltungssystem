import ApiService from './api.service';
import AuthService from './auth.service';

/**
 * Service für die Benutzerverwaltung
 * Fokussiert auf Benutzerdaten-Management, während AuthService die Authentifizierung handhabt
 */
class UserService {
  /**
   * Holt Informationen über den aktuellen Benutzer
   * @returns {Promise<Object>} Benutzerinformationen
   */
  static async getCurrentUser() {
    return await AuthService.getCurrentUser();
  }

  /**
   * Aktualisiert Benutzerdaten
   * @param {Object} userData - Zu aktualisierende Benutzerdaten
   * @returns {Promise<Object>} Aktualisierte Benutzerinformationen
   */
  static async updateUser(userData) {
    return await ApiService.put('/api/user', userData);
  }

  /**
   * Löscht den aktuellen Benutzer
   * @returns {Promise<Object>} Bestätigung der Löschung
   */
  static async deleteUser() {
    try {
      const response = await ApiService.delete('/api/user');
      // Nach erfolgreicher Löschung auch den Token entfernen
      AuthService.removeToken();
      localStorage.removeItem('access_token_exp');
      return response;
    } catch (error) {
      console.error('Fehler beim Löschen des Benutzers:', error);
      throw error;
    }
  }

  /**
   * Holt eine Liste aller Benutzer (Admin-Funktion)
   * @returns {Promise<Array>} Liste der Benutzer
   */
  static async getAllUsers() {
    return await ApiService.get('/api/users');
  }

  /**
   * Holt Informationen über einen bestimmten Benutzer (Admin-Funktion)
   * @param {number} userId - ID des Benutzers
   * @returns {Promise<Object>} Benutzerinformationen
   */
  static async getUserById(userId) {
    return await ApiService.get(`/api/users/${userId}`);
  }

  /**
   * Aktualisiert einen bestimmten Benutzer (Admin-Funktion)
   * @param {number} userId - ID des Benutzers
   * @param {Object} userData - Zu aktualisierende Benutzerdaten
   * @returns {Promise<Object>} Aktualisierte Benutzerinformationen
   */
  static async updateUserById(userId, userData) {
    return await ApiService.put(`/api/users/${userId}`, userData);
  }

  /**
   * Löscht einen bestimmten Benutzer (Admin-Funktion)
   * @param {number} userId - ID des zu löschenden Benutzers
   * @returns {Promise<Object>} Bestätigung der Löschung
   */
  static async deleteUserById(userId) {
    return await ApiService.delete(`/api/users/${userId}`);
  }
}

export default UserService;
