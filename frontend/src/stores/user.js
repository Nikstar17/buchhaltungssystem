import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    id: '',
    name: '',
    email: ''
  }),
  actions: {
    setId(id) {
      this.id = id;
    },
    setEmail(email) {
      this.email = email;
    },
    setName(name) {
      this.name = name;
    }
  }
});
