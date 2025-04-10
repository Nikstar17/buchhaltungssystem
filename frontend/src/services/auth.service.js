import ApiService from './api.service';
import { jwtDecode } from 'jwt-decode';

/**
 * Service zur Verwaltung der Authentifizierung und Benutzerdaten
 */
class AuthService {
  /**
   * Benutzer anmelden
   * @param {Object} credentials - Anmeldedaten (E-Mail und Passwort)
   * @returns {Promise<Object>} Anmeldeinformationen mit Token
   */
  static async login(credentials) {
    try {
      const response = await ApiService.post('/api/login', credentials);

      // Unterstützt sowohl token als auch access_token Format
      const token = response.token || response.access_token;

      if (token) {
        this.saveToken(token);

        // Token-Ablaufzeit direkt mit jwtDecode speichern
        if (typeof token === 'string') {
          try {
            const decodedToken = jwtDecode(token);
            if (decodedToken && decodedToken.exp) {
              localStorage.setItem('access_token_exp', decodedToken.exp * 1000);
            }
          } catch (decodeError) {
            // Wenn Dekodierung fehlschlägt, langer Ablaufzeitraum (1 Stunde)
            const oneHourFromNow = Date.now() + 60 * 60 * 1000;
            localStorage.setItem('access_token_exp', oneHourFromNow);
          }
        }
      }
      return response;
    } catch (error) {
      console.error('Anmeldefehler:', error);
      throw error;
    }
  }

  /**
   * Benutzer abmelden
   * @returns {Promise<Object>} Abmeldeinformationen
   */
  static async logout() {
    try {
      const response = await ApiService.post('/api/logout', {});
      this.removeToken();
      localStorage.removeItem('access_token_exp');
      return response;
    } catch (error) {
      console.error('Abmeldefehler:', error);
      // Auch bei Fehlern Token lokal entfernen
      this.removeToken();
      localStorage.removeItem('access_token_exp');
      throw error;
    }
  }

  /**
   * Token aktualisieren
   * @returns {Promise<Object>} Neues Token
   */
  static async refreshToken() {
    try {
      const response = await ApiService.post('/api/refresh', {});

      // Unterstützt sowohl token als auch access_token Format
      const token = response.token || response.access_token;

      if (token) {
        this.saveToken(token);

        // Token-Ablaufzeit direkt mit jwtDecode speichern
        if (typeof token === 'string') {
          try {
            const decodedToken = jwtDecode(token);
            if (decodedToken && decodedToken.exp) {
              localStorage.setItem('access_token_exp', decodedToken.exp * 1000);
            } else {
              // Fallback, wenn kein exp im Token vorhanden
              const oneHourFromNow = Date.now() + 60 * 60 * 1000;
              localStorage.setItem('access_token_exp', oneHourFromNow);
            }
          } catch (decodeError) {
            // Wenn Dekodierung fehlschlägt, langer Ablaufzeitraum (1 Stunde)
            const oneHourFromNow = Date.now() + 60 * 60 * 1000;
            localStorage.setItem('access_token_exp', oneHourFromNow);
          }
        }
      } else if (this.getToken()) {
        // Wenn kein neues Token, aber noch altes vorhanden
        // Setzen wir eine Kurzzeit-Ablaufzeit (5 Minuten)
        const fiveMinutesFromNow = Date.now() + 5 * 60 * 1000;
        localStorage.setItem('access_token_exp', fiveMinutesFromNow);
      }
      return response;
    } catch (error) {
      console.error('Fehler beim Aktualisieren des Tokens:', error);
      throw error;
    }
  }

  /**
   * Informationen des aktuell angemeldeten Benutzers abrufen
   * @returns {Promise<Object>} Benutzerinformationen
   */
  static async getCurrentUser() {
    try {
      return await ApiService.get('/api/user');
    } catch (error) {
      console.error('Fehler beim Abrufen des aktuellen Benutzers:', error);
      throw error;
    }
  }

  /**
   * Benutzer registrieren
   * @param {Object} userData - Benutzerdaten für die Registrierung
   * @returns {Promise<Object>} Registrierungsinformationen mit Token
   */
  static async register(userData) {
    try {
      const response = await ApiService.post('/api/register', userData);

      // Unterstützt sowohl token als auch access_token Format
      const token = response.token || response.access_token;

      if (token) {
        this.saveToken(token);

        // Token-Ablaufzeit speichern, wenn verfügbar
        if (typeof token === 'string') {
          try {
            const decodedToken = jwtDecode(token);
            if (decodedToken && decodedToken.exp) {
              localStorage.setItem('access_token_exp', decodedToken.exp * 1000);
            }
          } catch (error) {
            // Fallback wenn Token nicht dekodiert werden kann
          }
        }
      }
      return response;
    } catch (error) {
      console.error('Registrierungsfehler:', error);
      throw error;
    }
  }

  /**
   * Benutzerprofil aktualisieren
   * @param {Object} userData - Aktualisierte Benutzerdaten
   * @returns {Promise<Object>} Aktualisierte Benutzerinformationen
   */
  static async updateProfile(userData) {
    try {
      return await ApiService.put('/api/user', userData);
    } catch (error) {
      console.error('Fehler beim Aktualisieren des Benutzerprofils:', error);
      throw error;
    }
  }

  /**
   * Passwort ändern
   * @param {Object} passwordData - Altes und neues Passwort
   * @returns {Promise<Object>} Rückmeldung des Servers
   */
  static async changePassword(passwordData) {
    try {
      return await ApiService.post('/api/user/change-password', passwordData);
    } catch (error) {
      console.error('Fehler beim Ändern des Passworts:', error);
      throw error;
    }
  }

  /**
   * Überprüfen, ob ein Benutzer angemeldet ist
   * @returns {boolean} true, wenn ein Token vorhanden ist
   */
  static isLoggedIn() {
    return !!this.getToken();
  }

  /**
   * Überprüfen, ob ein Token abgelaufen ist
   * @returns {boolean} true, wenn das Token abgelaufen ist oder nicht vorhanden
   */
  static isTokenExpired() {
    const token = this.getToken();
    if (!token) {
      return true;
    }

    const expTime = parseInt(localStorage.getItem('access_token_exp'));
    if (!expTime) {
      // Wenn keine Ablaufzeit gespeichert ist, versuche sie aus dem Token zu extrahieren
      try {
        const decodedToken = jwtDecode(token);
        if (decodedToken && decodedToken.exp) {
          const expDate = decodedToken.exp * 1000;
          localStorage.setItem('access_token_exp', expDate);
          return Date.now() > expDate - 5000;
        }
      } catch (error) {
        // Token kann nicht dekodiert werden, nehmen wir an, es ist gültig
        return false;
      }
      return false;
    }

    // 5 Sekunden Puffer hinzufügen
    return Date.now() > expTime - 5000;
  }

  /**
   * Token aus dem localStorage abrufen
   * @returns {string|null} Token oder null, wenn kein Token vorhanden
   */
  static getToken() {
    return localStorage.getItem('token');
  }

  /**
   * Token im localStorage speichern
   * @param {string} token - Das zu speichernde Token
   */
  static saveToken(token) {
    localStorage.setItem('token', token);
  }

  /**
   * Token aus dem localStorage entfernen
   */
  static removeToken() {
    localStorage.removeItem('token');
  }
}

export default AuthService;
