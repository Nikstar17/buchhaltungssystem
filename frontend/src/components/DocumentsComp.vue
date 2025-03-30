<template>
  <div class="flex min-h-screen">
    <main class="flex-1 p-6">
      <div class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
        <button
          @click="showUploadModal = true"
          class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700"
        >
          ➕ Beleg hochladen
        </button>
        <div class="flex space-x-2">
          <input type="text" placeholder="🔍 Suche..." class="px-3 py-2 rounded border border-gray-300" />
          <input type="month" class="px-3 py-2 rounded border border-gray-300" />
        </div>
      </div>

      <div class="bg-white shadow rounded-xl overflow-hidden">
        <table class="min-w-full text-sm text-left">
          <thead class="bg-gray-100 border-b font-semibold">
            <tr>
              <th class="px-4 py-3">Datum</th>
              <th class="px-4 py-3">Name</th>
              <th class="px-4 py-3">Kategorie</th>
              <th class="px-4 py-3">Betrag</th>
              <th class="px-4 py-3">Aktionen</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-b hover:bg-gray-50">
              <td class="px-4 py-3">02.03.2025</td>
              <td class="px-4 py-3">Rechnung A</td>
              <td class="px-4 py-3">Einnahme</td>
              <td class="px-4 py-3">300,00 €</td>
              <td class="px-4 py-3 space-x-2">
                <button class="text-blue-600 hover:underline">Ansehen</button>
                <button class="text-green-600 hover:underline">Bearbeiten</button>
                <button class="text-red-600 hover:underline">Löschen</button>
              </td>
            </tr>
            <tr class="border-b hover:bg-gray-50">
              <td class="px-4 py-3">01.03.2025</td>
              <td class="px-4 py-3">Kassenbon Supermarkt</td>
              <td class="px-4 py-3">Lebensmittel</td>
              <td class="px-4 py-3">45,00 €</td>
              <td class="px-4 py-3 space-x-2">
                <button class="text-blue-600 hover:underline">Ansehen</button>
                <button class="text-green-600 hover:underline">Bearbeiten</button>
                <button class="text-red-600 hover:underline">Löschen</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Modal -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
        <button @click="showUploadModal = false" class="absolute top-4 right-4 text-red-500 hover:text-gray-500">
          <div class="bg-gray-200 rounded-full p-2">
            <XMarkIcon class="w-8 h-8 text-red-600 hover:text-gray-500" />
          </div>
        </button>
        <DocumentUpload />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import DocumentUpload from './DocumentUpload.vue';
import { XMarkIcon } from '@heroicons/vue/24/solid'; // Import Heroicon

const showUploadModal = ref(false);
</script>

<style scoped></style>
