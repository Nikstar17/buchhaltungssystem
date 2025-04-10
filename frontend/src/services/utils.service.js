/**
 * Service mit nützlichen Hilfsfunktionen für die gesamte Anwendung
 */
class UtilsService {
  /**
   * Formatiert einen Betrag als Währung
   * @param {number} amount - Der zu formatierende Betrag
   * @param {string} locale - Das zu verwendende Gebietsschema, Standard: 'de-DE'
   * @param {string} currency - Die zu verwendende Währung, Standard: 'EUR'
   * @returns {string} Formatierter Währungsbetrag
   */
  static formatCurrency(amount, locale = 'de-DE', currency = 'EUR') {
    if (amount === null || amount === undefined) return '-';
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency,
    }).format(amount);
  }

  /**
   * Formatiert ein Datum im deutschen Format
   * @param {string|Date} date - Das zu formatierende Datum
   * @param {Object} options - Formatierungsoptionen für toLocaleDateString
   * @returns {string} Formatiertes Datum
   */
  static formatDate(date, options = { day: '2-digit', month: '2-digit', year: 'numeric' }) {
    if (!date) return '-';
    return new Date(date).toLocaleDateString('de-DE', options);
  }

  /**
   * Berechnet die verbleibenden Tage bis zu einem Datum
   * @param {string|Date} dueDate - Das Fälligkeitsdatum
   * @returns {string} Beschreibung der verbleibenden Zeit oder des Überfälligkeitsstatus
   */
  static calculateDaysUntilDue(dueDate) {
    if (!dueDate) return '-';

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const due = new Date(dueDate);
    due.setHours(0, 0, 0, 0);

    const diffTime = due - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
      return `${Math.abs(diffDays)} Tage überfällig`;
    } else if (diffDays === 0) {
      return 'Heute fällig';
    } else if (diffDays === 1) {
      return 'Morgen fällig';
    } else {
      return `In ${diffDays} Tagen fällig`;
    }
  }

  /**
   * Validiert eine Emailadresse
   * @param {string} email - Die zu validierende Emailadresse
   * @returns {boolean} true, wenn die Emailadresse gültig ist
   */
  static isValidEmail(email) {
    const re =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
  }

  /**
   * Validiert eine Steuernummer
   * @param {string} taxNumber - Die zu validierende Steuernummer
   * @returns {boolean} true, wenn die Steuernummer gültig ist
   */
  static isValidTaxNumber(taxNumber) {
    // Einfache Prüfung auf korrektes deutsches Steuernummer-Format
    // (Dies ist eine vereinfachte Prüfung, in der Praxis wären komplexere Regeln nötig)
    return /^\d{2}\/\d{3}\/\d{5}$/.test(taxNumber);
  }

  /**
   * Validiert eine Umsatzsteuer-ID
   * @param {string} vatId - Die zu validierende USt-ID
   * @returns {boolean} true, wenn die USt-ID gültig ist
   */
  static isValidVatId(vatId) {
    // Einfache Prüfung auf korrektes EU-USt-ID-Format
    // (Dies ist eine vereinfachte Prüfung, in der Praxis wären komplexere Regeln nötig)
    return /^DE\d{9}$/.test(vatId);
  }

  /**
   * Generiert eine zufällige ID
   * @param {number} length - Die Länge der zu generierenden ID, Standard: 8
   * @returns {string} Generierte ID
   */
  static generateRandomId(length = 8) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let id = '';

    for (let i = 0; i < length; i++) {
      id += chars.charAt(Math.floor(Math.random() * chars.length));
    }

    return id;
  }

  /**
   * Konvertiert einen String in Title Case (jedes Wort beginnt mit einem Großbuchstaben)
   * @param {string} text - Der zu konvertierende String
   * @returns {string} Konvertierter String
   */
  static toTitleCase(text) {
    if (!text) return '';
    return text.replace(
      /\w\S*/g,
      (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
    );
  }

  /**
   * Kürzt einen String, wenn er länger ist als die angegebene Länge
   * @param {string} text - Der zu kürzende String
   * @param {number} maxLength - Die maximale Länge, Standard: 50
   * @returns {string} Gekürzter String mit Ellipsis
   */
  static truncateText(text, maxLength = 50) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }
}

export default UtilsService;
