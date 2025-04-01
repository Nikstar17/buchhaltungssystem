<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <form
      @submit.prevent="register"
      id="registerForm"
      class="bg-white p-6 rounded-lg shadow-md w-full max-w-sm"
    >
      <h2 class="text-2xl font-bold mb-4 text-center">Registrieren</h2>

      <div class="mb-4">
        <input
          type="email"
          v-model="email"
          name="email"
          placeholder="Email"
          required
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div class="mb-4">
        <input
          type="password"
          v-model="password"
          name="password"
          placeholder="Password"
          required
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Vorname und Nachname nebeneinander -->
      <div class="flex space-x-4 mb-4">
        <input
          type="text"
          v-model="first_name"
          name="first_name"
          placeholder="Vorname"
          required
          class="w-1/2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          v-model="last_name"
          name="last_name"
          placeholder="Nachname"
          required
          class="w-1/2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div class="flex space-x-4 mb-4">
        <input
          type="text"
          v-model="street"
          name="street"
          placeholder="Straße"
          required
          class="w-3/4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          v-model="house_number"
          name="house_number"
          placeholder="Nr."
          pattern="^[0-9]+[a-zA-Z\-\/]?$"
          required
          class="w-1/4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div class="flex space-x-4 mb-4">
        <input
          type="text"
          v-model="postal_code"
          name="postal_code"
          placeholder="PLZ"
          required
          class="w-1/4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          v-model="city"
          name="city"
          placeholder="Stadt"
          required
          class="w-3/4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div class="mb-4">
        <input
          type="text"
          v-model="country"
          name="country"
          placeholder="Land"
          required
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <button
        type="submit"
        class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition"
      >
        Registrieren
      </button>
      <p class="mt-6 text-center text-sm text-gray-600">
        Noch kein Konto?
        <router-link to="/login" class="text-blue-600 hover:underline">Hier einloggen</router-link>
      </p>
    </form>
    <!-- Snackbar -->
    <div
      v-if="showSnackbar"
      :class="snackbarType === 'success' ? 'bg-green-700' : 'bg-red-700'"
      class="fixed top-4 left-1/2 transform -translate-x-1/2 text-white px-4 py-2 rounded shadow-lg transition-opacity duration-300"
    >
      {{ snackbarMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import API_URL from '@/api';
import { useRouter } from 'vue-router';
import {
  showSnackbar,
  snackbarMessage,
  snackbarType,
  showSnackbarMessage,
} from '@/composables/useSnackbar';

const email = ref('');
const password = ref('');
const first_name = ref('');
const last_name = ref('');
const street = ref('');
const house_number = ref('');
const postal_code = ref('');
const city = ref('');
const country = ref('');

const router = useRouter();

const register = async () => {
  try {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
        first_name: first_name.value,
        last_name: last_name.value,
        street: street.value,
        house_number: house_number.value,
        postal_code: postal_code.value,
        city: city.value,
        country: country.value,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      localStorage.setItem('access_token', result.access_token);
      showSnackbarMessage('Registrierung erfolgreich!', 'success');
      await new Promise((resolve) => setTimeout(resolve, 2000));
      router.push({ name: 'login' });
    } else if (response.status === 409) {
      showSnackbarMessage('Diese E-Mail-Adresse ist bereits registriert.', 'error');
    } else {
      showSnackbarMessage('Fehler bei der Registrierung', 'error');
    }
  } catch (error) {
    showSnackbarMessage('Fehler bei der Registrierung', 'error');
  }
};
</script>

<style scoped></style>
