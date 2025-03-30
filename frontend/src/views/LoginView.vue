<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md">
      <form @submit.prevent="login" id="loginForm" class="space-y-6">
        <h1 class="text-2xl font-bold text-gray-800 text-center">Anmelden</h1>
        <input
          type="email"
          v-model="email"
          placeholder="Email"
          id="email"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          id="password"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          class="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Login
        </button>
      </form>
      <p class="mt-6 text-center text-sm text-gray-600">
        Noch kein Konto?
        <a href="/register" class="text-blue-600 hover:underline">Hier registrieren</a>
      </p>
    </div>
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

const login = async () => {
  const response = await fetch(`${API_URL}/login`, {
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
    router.push({ name: 'home' });
  } else {
    message.value = result.message || 'Fehler bei der Anmeldung';
    alert(message.value);
  }
};
</script>

<style scoped></style>
