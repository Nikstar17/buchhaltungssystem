import { ref } from 'vue';

export const snackbarMessage = ref('');
export const snackbarType = ref('info');
export const showSnackbar = ref(false);

/**
 * Zeigt eine Snackbar-Nachricht mit Typ und Dauer
 * @param {string} message - Die Nachricht, die angezeigt wird
 * @param {'success' | 'error' | 'info'} type - Der Typ der Snackbar
 * @param {number} duration - Dauer in ms, wie lange die Snackbar angezeigt wird
 */
export function showSnackbarMessage(message, type = 'info', duration = 5000) {
  snackbarMessage.value = message;
  snackbarType.value = type;
  showSnackbar.value = true;

  setTimeout(() => {
    showSnackbar.value = false;
  }, duration);
}
