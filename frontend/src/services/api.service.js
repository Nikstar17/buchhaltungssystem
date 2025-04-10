import API_URL from '@/api';

/**
 * Basis-Service für API-Anfragen
 * Zentralisiert die API-Kommunikation und behandelt allgemeine Fehler
 */
class ApiService {
  /**
   * Allgemeine GET-Anfrage
   * @param {string} endpoint - API-Endpunkt
   * @returns {Promise<any>} - Die Antwortdaten
   */
  static async get(endpoint) {
    try {
      const csrfToken = this.getCsrfToken();
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'X-CSRF-TOKEN': csrfToken,
        },
      });

      return await this.handleResponse(response);
    } catch (error) {
      throw error;
    }
  }

  /**
   * Allgemeine POST-Anfrage
   * @param {string} endpoint - API-Endpunkt
   * @param {Object} data - Die zu sendenden Daten
   * @returns {Promise<any>} - Die Antwortdaten
   */
  static async post(endpoint, data) {
    try {
      // Spezielle Behandlung für Token-Refresh
      if (endpoint === '/api/refresh') {
        return this.refreshToken();
      }

      const csrfToken = this.getCsrfToken();
      const headers = {
        'X-CSRF-TOKEN': csrfToken,
      };

      // Bei FormData kein Content-Type Header setzen, wird automatisch gesetzt
      if (!(data instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
      }

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        credentials: 'include',
        headers,
        body: data instanceof FormData ? data : JSON.stringify(data),
      });

      return await this.handleResponse(response);
    } catch (error) {
      throw error;
    }
  }

  /**
   * Allgemeine PUT-Anfrage
   * @param {string} endpoint - API-Endpunkt
   * @param {Object} data - Die zu sendenden Daten
   * @returns {Promise<any>} - Die Antwortdaten
   */
  static async put(endpoint, data) {
    try {
      const csrfToken = this.getCsrfToken();

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrfToken,
        },
        body: JSON.stringify(data),
      });

      return await this.handleResponse(response);
    } catch (error) {
      throw error;
    }
  }

  /**
   * Allgemeine DELETE-Anfrage
   * @param {string} endpoint - API-Endpunkt
   * @returns {Promise<any>} - Die Antwortdaten
   */
  static async delete(endpoint) {
    try {
      const csrfToken = this.getCsrfToken();

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
          'X-CSRF-TOKEN': csrfToken,
        },
      });

      return await this.handleResponse(response);
    } catch (error) {
      throw error;
    }
  }

  /**
   * Einheitliche Behandlung von API-Antworten
   * @param {Response} response - Fetch API Response-Objekt
   * @returns {Promise<any>} - Die verarbeiteten Antwortdaten
   */
  static async handleResponse(response) {
    if (!response.ok) {
      const errorText = await response.text();
      try {
        const errorData = JSON.parse(errorText);
        throw new Error(errorData.message || errorData.msg || `HTTP-Fehler: ${response.status}`);
      } catch (jsonError) {
        throw new Error(`HTTP-Fehler: ${response.status} - ${errorText}`);
      }
    }

    return response.status === 204 ? {} : await response.json();
  }

  /**
   * Hilfsmethode zum Extrahieren des CSRF-Tokens aus Cookies
   * @param {string} [type='access'] - 'access' oder 'refresh', um den spezifischen Token-Typ zu bekommen
   * @returns {string} CSRF-Token oder leerer String
   */
  static getCsrfToken(type = 'access') {
    // Prioritätsliste für Token-Namen basierend auf dem Typ
    let tokenNames = [];

    if (type === 'refresh') {
      tokenNames = ['csrf_refresh_token', 'csrf_access_token', 'csrf_token'];
    } else {
      tokenNames = ['csrf_access_token', 'csrf_token', 'csrf_refresh_token'];
    }

    // Versuche die Token-Namen in der angegebenen Reihenfolge
    for (const name of tokenNames) {
      const cookieValue = document.cookie.split('; ').find((row) => row.startsWith(`${name}=`));

      if (cookieValue) {
        const token = cookieValue.split('=')[1];
        try {
          return decodeURIComponent(token);
        } catch {
          return token;
        }
      }
    }

    // Fallback: Wenn kein spezifischer Token gefunden wurde, suche nach jedem CSRF-Token
    const allCsrfCookies = document.cookie
      .split('; ')
      .filter((row) => row.toLowerCase().startsWith('csrf_'));

    if (allCsrfCookies.length > 0) {
      const token = allCsrfCookies[0].split('=')[1];
      try {
        return decodeURIComponent(token);
      } catch {
        return token;
      }
    }

    return '';
  }

  /**
   * Speziell für Token-Refresh-Anfragen
   * @returns {Promise<any>} - Die Antwortdaten
   */
  static async refreshToken() {
    try {
      // Speziell den Refresh-CSRF-Token abrufen
      const refreshCsrfToken = this.getCsrfToken('refresh');

      if (!refreshCsrfToken) {
        throw new Error('Kein CSRF-Token für Refresh vorhanden');
      }

      // Wichtig: Exakter Pfad wie vom Backend erwartet
      const response = await fetch(`${API_URL}/api/refresh`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'X-CSRF-TOKEN': refreshCsrfToken,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      return await this.handleResponse(response);
    } catch (error) {
      throw error;
    }
  }

  /**
   * Speichert die Token-Ablaufzeit im localStorage
   * @param {string} token - JWT-Token
   */
  static saveTokenExpiration(token) {
    try {
      // Nur ausführen, wenn der jwtDecode Wert existiert
      if (typeof jwtDecode === 'function' && token) {
        const tokenData = jwtDecode(token);
        if (tokenData && tokenData.exp) {
          localStorage.setItem('access_token_exp', tokenData.exp * 1000);
        }
      }
    } catch (error) {}
  }
}

export default ApiService;
