import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    id: '',
    first_name: '',
    last_name: '',
    email: ''
  }),
  actions: {
    setId(id) {
      this.id = id;
    },
    setEmail(email) {
      this.email = email;
    },
    setFirstName(first_name) {
      this.first_name = first_name
    },
    setLastName(last_name) {
      this.last_name = last_name
    }
  }
});
