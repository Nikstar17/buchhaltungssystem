<template>
  <div class="flex min-h-screen">
    <main class="flex-1 p-6">
      <div class="mb-6 flex flex-row justify-between space-y-4 md:space-y-0">
        <RouterLink
          :to="{ name: 'journal-entry-form' }"
          class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 flex items-center space-x-2"
        >
          <PlusIcon class="w-5 h-5" />
          <span>Neue Buchung</span>
        </RouterLink>
        <div class="flex space-x-2">
          <input
            type="text"
            placeholder="🔍 Suche..."
            class="px-3 py-2 rounded border border-gray-300"
          />
          <input type="month" class="px-3 py-2 rounded border border-gray-300" />
        </div>
      </div>
      <!-- TODO: Tabelle aller Buchungen -->
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { PlusIcon } from '@heroicons/vue/24/solid';
import API_URL from '@/api';
</script>

<style scoped></style>
