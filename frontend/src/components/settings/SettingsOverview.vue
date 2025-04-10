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
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full">
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-blue-100 rounded-lg">
                <UserIcon class="w-5 h-5" />
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Benutzerprofil</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">
              Bearbeiten Sie Ihre persönlichen Daten und Kontoinformationen
            </p>
            <RouterLink :to="{ name: 'user-settings' }"
              class="w-full px-4 py-2 bg-blue-50 text-blue-600 rounded-lg border border-blue-100 hover:bg-blue-100 transition-colors duration-200 flex justify-center items-center">
              <span>Profil bearbeiten</span>
              <ChevronRightIcon class="size-4" />
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Kontenplan Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full">
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-green-100 rounded-lg">
                <CalculatorIcon class="w-5 h-5" />
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Kontenplan</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Konfigurieren Sie Ihren Kontenplan und Buchungsregeln</p>
            <RouterLink :to="{ name: 'settings-chart-of-accounts' }"
              class="w-full px-4 py-2 bg-blue-50 text-blue-600 rounded-lg border border-blue-100 hover:bg-blue-100 transition-colors duration-200 flex justify-center items-center">
              <span>Profil bearbeiten</span>
              <ChevronRightIcon class="size-4" />
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Steuersätze Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full">
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-purple-100 rounded-lg">
                <CurrencyDollarIcon class="w-5 h-5" />
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Steuersätze</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Verwalten Sie die Steuersätze für Ihre Buchhaltung</p>
            <button
              class="w-full px-4 py-2 bg-purple-50 text-purple-600 rounded-lg border border-purple-100 hover:bg-purple-100 transition-colors duration-200 flex justify-center items-center">
              <span>Steuersätze bearbeiten</span>
              <ChevronRightIcon class="size-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Lieferanten & Kunden Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full">
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-yellow-100 rounded-lg">
                <UserGroupIcon class="w-5 h-5" />
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Lieferanten & Kunden</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Verwalten Sie Ihre Kunden- und Lieferantendaten</p>
            <button
              class="w-full px-4 py-2 bg-yellow-50 text-yellow-600 rounded-lg border border-yellow-100 hover:bg-yellow-100 transition-colors duration-200 flex justify-center items-center">
              <span>Kontakte verwalten</span>
              <ChevronRightIcon class="size-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Währungen Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full">
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-red-100 rounded-lg">
                <HashtagIcon class="w-5 h-5" />
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Währungen</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Konfigurieren Sie Währungen und Wechselkurse</p>
            <button
              class="w-full px-4 py-2 bg-red-50 text-red-600 rounded-lg border border-red-100 hover:bg-red-100 transition-colors duration-200 flex justify-center items-center">
              <span>Währungen bearbeiten</span>
              <ChevronRightIcon class="size-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Import/Export Karte -->
      <div class="w-1/2 md:w-1/2 px-3 mb-6">
        <div
          class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden h-full">
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-indigo-100 rounded-lg">
                <ArrowsRightLeftIcon class="w-5 h-5" />
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Import/Export</h2>
            </div>
          </div>
          <div class="p-5">
            <p class="text-gray-600 mb-4">Daten importieren oder exportieren (CSV, DATEV, etc.)</p>
            <button
              class="w-full px-4 py-2 bg-indigo-50 text-indigo-600 rounded-lg border border-indigo-100 hover:bg-indigo-100 transition-colors duration-200 flex justify-center items-center">
              <span>Import/Export starten</span>
              <ChevronRightIcon class="size-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Import von benötigten Komponenten und Funktionen
import { ChevronRightIcon } from '@heroicons/vue/24/solid';
import { UserIcon } from '@heroicons/vue/24/outline';
import { CalculatorIcon } from '@heroicons/vue/24/outline';
import { CurrencyDollarIcon } from '@heroicons/vue/24/outline'
import { UserGroupIcon } from '@heroicons/vue/24/outline'
import { HashtagIcon } from '@heroicons/vue/24/outline'
import { ArrowsRightLeftIcon } from '@heroicons/vue/24/outline'
</script>

<style scoped></style>
