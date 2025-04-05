<template>
  <div class="flex h-screen">
    <aside class="w-56 bg-white shadow-md p-4 flex flex-col justify-between h-screen">
      <div class="space-y-4">
        <h1 class="text-2xl font-bold text-blue-600">📘 Buchhaltung</h1>
        <nav class="flex flex-col space-y-2">
          <RouterLink :to="{ name: 'dashboard-overview' }">📊 Dashboard</RouterLink>
          <RouterLink :to="{ name: 'documents' }">📎 Belege</RouterLink>
          <RouterLink :to="{ name: 'journal-entry' }">💸 Buchungen</RouterLink>
          <a href="#" class="flex items-center space-x-2 hover:text-blue-600">
            <span>🏷️</span><span>Kategorien</span>
          </a>
          <a href="#" class="flex items-center space-x-2 hover:text-blue-600">
            <span>🏦</span><span>Konten</span>
          </a>
          <a href="#" class="flex items-center space-x-2 hover:text-blue-600">
            <span>📊</span><span>Auswertungen</span>
          </a>
          <a href="#" class="flex items-center space-x-2 hover:text-blue-600">
            <span>⚙️</span><span>Einstellungen</span>
          </a>
        </nav>
      </div>
      <div class="mt-auto pt-4 border-t">
        <span class="text-gray-600 block mb-2">👤 Max Mustermann</span>
        <button @click="logout" class="bg-red-100 text-red-600 px-3 py-1 rounded">Logout</button>
      </div>
    </aside>
    <main class="flex-1">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import API_URL from '@/api'; // API_URL importieren
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = async () => {
  await fetch(`${API_URL}/logout`, {
    method: 'POST',
    credentials: 'include', // Cookies werden mitgesendet
  });
  router.push({ name: 'login' });
};
</script>

<style scoped></style>
