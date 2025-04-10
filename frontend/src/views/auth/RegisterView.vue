<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <form @submit.prevent="register" id="registerForm" class="bg-white p-6 rounded-lg shadow-md w-full max-w-sm">
      <h2 class="text-2xl font-bold mb-4 text-center">Registrieren</h2>

      <div class="mb-4">
        <input type="email" v-model="email" name="email" placeholder="Email" required
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div class="mb-4">
        <input type="password" v-model="password" name="password" placeholder="Password" required
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <!-- Vorname und Nachname nebeneinander -->
      <div class="flex space-x-4 mb-4">
        <input type="text" v-model="first_name" name="first_name" placeholder="Vorname" required
          class="w-1/2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        <input type="text" v-model="last_name" name="last_name" placeholder="Nachname" required
          class="w-1/2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div class="flex space-x-4 mb-4">
        <input type="text" v-model="street" name="street" placeholder="Straße" required
          class="w-3/4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        <input type="text" v-model="house_number" name="house_number" placeholder="Nr." pattern="^[0-9]+[a-zA-Z\-\/]?$"
          required class="w-1/4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div class="flex space-x-4 mb-4">
        <input type="text" v-model="postal_code" name="postal_code" placeholder="PLZ" required
          class="w-1/4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        <input type="text" v-model="city" name="city" placeholder="Stadt" required
          class="w-3/4 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div class="mb-4">
        <input type="text" v-model="country" name="country" placeholder="Land" required
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <button type="submit" class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition">
        Registrieren
      </button>
      <p class="mt-6 text-center text-sm text-gray-600">
        Noch kein Konto?
        <router-link to="/login" class="text-blue-600 hover:underline">Hier einloggen</router-link>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import API_URL from '@/api';
import { useRouter } from 'vue-router';
import { showSnackbarMessage } from '@/composables/useSnackbar';
import { AuthService } from '@/services';

const router = useRouter();

const email = ref('');
const password = ref('');
const first_name = ref('');
const last_name = ref('');
const street = ref('');
const house_number = ref('');
const postal_code = ref('');
const city = ref('');
const country = ref('');

const register = async () => {
  try {
    const credentials = {
      email: email.value,
      password: password.value,
      first_name: first_name.value,
      last_name: last_name.value,
      street: street.value,
      house_number: house_number.value,
      postal_code: postal_code.value,
      city: city.value,
      country: country.value,
    };

    await AuthService.register(credentials);
    router.push({ name: 'dashboard-overview' });
    showSnackbarMessage('Herzlich Willkommen', 'success');
  } catch (error) {
    console.log(error)
    showSnackbarMessage('Fehler beim registrieren', error);
  }
};
</script>

<style scoped></style>
