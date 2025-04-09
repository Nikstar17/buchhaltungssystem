<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-2">Einstellungen</h1>
      <p class="text-gray-600">Verwalten Sie Ihre Benutzereinstellungen und Systemkonfiguration</p>
    </div>

    <!-- Verwenden eines Flex-Layouts anstelle eines Grid-Layouts -->
    <div class="flex flex-wrap -mx-3">
      <!-- Benutzerprofil Karte -->
      <div class="w-1/2 md:w-full px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full"
        >
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-blue-100 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-blue-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Benutzerprofil</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">
              Bearbeiten Sie Ihre persönlichen Daten und Kontoinformationen
            </p>
            <RouterLink
              :to="{ name: 'user-settings' }"
              class="w-full px-4 py-2 bg-blue-50 text-blue-600 rounded-lg border border-blue-100 hover:bg-blue-100 transition-colors duration-200 flex justify-center items-center"
            >
              <span>Profil bearbeiten</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 ml-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Kontenplan Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full"
        >
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-green-100 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-green-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Kontenplan</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Konfigurieren Sie Ihren Kontenplan und Buchungsregeln</p>
            <button
              class="w-full px-4 py-2 bg-green-50 text-green-600 rounded-lg border border-green-100 hover:bg-green-100 transition-colors duration-200 flex justify-center items-center"
            >
              <span>Kontenplan verwalten</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 ml-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Steuersätze Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full"
        >
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-purple-100 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-purple-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Steuersätze</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Verwalten Sie die Steuersätze für Ihre Buchhaltung</p>
            <button
              class="w-full px-4 py-2 bg-purple-50 text-purple-600 rounded-lg border border-purple-100 hover:bg-purple-100 transition-colors duration-200 flex justify-center items-center"
            >
              <span>Steuersätze bearbeiten</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 ml-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Lieferanten & Kunden Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full"
        >
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-yellow-100 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-yellow-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Lieferanten & Kunden</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Verwalten Sie Ihre Kunden- und Lieferantendaten</p>
            <button
              class="w-full px-4 py-2 bg-yellow-50 text-yellow-600 rounded-lg border border-yellow-100 hover:bg-yellow-100 transition-colors duration-200 flex justify-center items-center"
            >
              <span>Kontakte verwalten</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 ml-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Währungen Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full"
        >
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-red-100 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"
                  />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Währungen</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Konfigurieren Sie Währungen und Wechselkurse</p>
            <button
              class="w-full px-4 py-2 bg-red-50 text-red-600 rounded-lg border border-red-100 hover:bg-red-100 transition-colors duration-200 flex justify-center items-center"
            >
              <span>Währungen bearbeiten</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 ml-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Import/Export Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full"
        >
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-indigo-100 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-indigo-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"
                  />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Import/Export</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Daten importieren oder exportieren (CSV, DATEV, etc.)</p>
            <button
              class="w-full px-4 py-2 bg-indigo-50 text-indigo-600 rounded-lg border border-indigo-100 hover:bg-indigo-100 transition-colors duration-200 flex justify-center items-center"
            >
              <span>Import/Export starten</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 ml-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Import von benötigten Komponenten und Funktionen
import { useRouter } from 'vue-router';

const router = useRouter();

// Funktionen zum Navigieren zu den Einstellungen können hier hinzugefügt werden
</script>

<style scoped>
/* Benutzerdefinierte Stile können hier hinzugefügt werden */
</style>
