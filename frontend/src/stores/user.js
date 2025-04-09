import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => {
    // Versuche, gespeicherte Daten aus dem localStorage zu laden
    const savedUser = localStorage.getItem('userData');
    if (savedUser) {
      try {
        return JSON.parse(savedUser);
      } catch (error) {
        console.error('Fehler beim Laden des Benutzers aus localStorage:', error);
      }
    }
    // Fallback zu leeren Werten
    return {
      id: '',
      first_name: '',
      last_name: '',
      email: '',
    };
  },
  actions: {
    setId(id) {
      this.id = id;
      this.saveToLocalStorage();
    },
    setEmail(email) {
      this.email = email;
      this.saveToLocalStorage();
    },
    setFirstName(first_name) {
      this.first_name = first_name;
      this.saveToLocalStorage();
    },
    setLastName(last_name) {
      this.last_name = last_name;
      this.saveToLocalStorage();
    },
    saveToLocalStorage() {
      localStorage.setItem(
        'userData',
        JSON.stringify({
          id: this.id,
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
        })
      );
    },
    clearUserData() {
      this.id = '';
      this.first_name = '';
      this.last_name = '';
      this.email = '';
      localStorage.removeItem('userData');
    },
  },
});
