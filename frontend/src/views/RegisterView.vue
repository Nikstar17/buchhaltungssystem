<template>
  <div>
    <form @submit.prevent="register" id="registerForm">
      <input type="email" v-model="email" placeholder="Email" id="email" />
      <input type="password" v-model="password" placeholder="Password" id="password" />
      <button type="submit">Registrieren</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import API_URL from '@/api';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const message = ref('');
const router = useRouter();

const register = async () => {
  try {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    });

    const result = await response.json();

    if (response.ok) {
      localStorage.setItem('access_token', result.access_token);
      router.push({ name: 'dashboard' });
    } else {
      message.value = result.error || 'Fehler bei der Anmeldung';
      alert(message.value);
    }
  } catch (error) {
    console.error('Fehler beim Registrieren:', error);
    alert('Ein unerwarteter Fehler ist aufgetreten.');
  }
};
</script>

<style scoped></style>
