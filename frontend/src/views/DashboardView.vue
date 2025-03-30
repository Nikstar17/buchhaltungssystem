<template>
  <div class="flex min-h-screen">
    <aside class="w-64 bg-white shadow-md p-4 space-y-4">
      <h1 class="text-2xl font-bold text-blue-600">📘 Buchhaltung</h1>
      <nav class="flex flex-col space-y-2">
        <RouterLink to="/dashboard/home">📊 Dashboard</RouterLink>
        <RouterLink to="/dashboard/documents">📎 Belege</RouterLink>
        <a href="#" class="flex items-center space-x-2 hover:text-blue-600"> <span>💸</span><span>Buchungen</span> </a>
        <a href="#" class="flex items-center space-x-2 hover:text-blue-600"> <span>🏷️</span><span>Kategorien</span> </a>
        <a href="#" class="flex items-center space-x-2 hover:text-blue-600"> <span>🏦</span><span>Konten</span> </a>
        <a href="#" class="flex items-center space-x-2 hover:text-blue-600">
          <span>📊</span><span>Auswertungen</span>
        </a>
        <a href="#" class="flex items-center space-x-2 hover:text-blue-600">
          <span>⚙️</span><span>Einstellungen</span>
        </a>
      </nav>
    </aside>

    <main class="flex-1 p-6">
      <div class="flex justify-end items-center mb-6">
        <div class="flex items-center space-x-4">
          <span class="text-gray-600">👤 Max Mustermann</span>
          <button @click="$router.push('/logout')" class="bg-red-100 text-red-600 px-3 py-1 rounded">Logout</button>
        </div>
      </div>
      <RouterView />
    </main>
  </div>
</template>

<script setup></script>

<style scoped></style>
