<template>
  <div>
    <!-- Modal für neuen Lieferanten -->
    <div
      v-if="showSupplierModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in"
    >
      <div class="bg-white p-6 rounded-xl shadow-lg w-1/3 max-w-md animate-scale-in">
        <h2 class="text-lg font-bold mb-4 text-gray-800">Neuen Lieferanten hinzufügen</h2>
        <form @submit.prevent="addNewSupplier" class="space-y-4">
          <div class="space-y-2">
            <label for="supplierName" class="block text-sm font-semibold text-gray-700"
              >Name des Lieferanten *</label
            >
            <input
              type="text"
              id="supplierName"
              v-model="newSupplier.name"
              required
              placeholder="Lieferantenname eingeben"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            />
          </div>

          <div class="space-y-2">
            <label for="supplierAddress" class="block text-sm font-semibold text-gray-700"
              >Adresse *</label
            >
            <input
              type="text"
              id="supplierAddress"
              v-model="newSupplier.address"
              required
              placeholder="Adresse eingeben"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            />
          </div>

          <div class="space-y-2">
            <label for="supplierTaxnumber" class="block text-sm font-semibold text-gray-700"
              >Steuernummer</label
            >
            <input
              type="text"
              id="supplierTaxnumber"
              v-model="newSupplier.tax_number"
              placeholder="Steuernummer eingeben"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            />
          </div>

          <div class="space-y-2">
            <label for="supplierVatId" class="block text-sm font-semibold text-gray-700"
              >USt-IdNr.</label
            >
            <input
              type="text"
              id="supplierVatId"
              v-model="newSupplier.vat_id"
              placeholder="USt-IdNr. eingeben"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            />
          </div>

          <div class="space-y-2">
            <label for="supplierIban" class="block text-sm font-semibold text-gray-700">IBAN</label>
            <input
              type="text"
              id="supplierIban"
              v-model="newSupplier.iban"
              placeholder="IBAN eingeben"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            />
          </div>

          <div class="space-y-2">
            <label for="supplierBic" class="block text-sm font-semibold text-gray-700">BIC</label>
            <input
              type="text"
              id="supplierBic"
              v-model="newSupplier.bic"
              placeholder="BIC eingeben"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            />
          </div>

          <div class="space-y-2">
            <label for="supplierEmail" class="block text-sm font-semibold text-gray-700"
              >E-Mail</label
            >
            <input
              type="text"
              id="supplierEmail"
              v-model="newSupplier.email"
              placeholder="E-Mail eingeben"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            />
          </div>

          <div class="space-y-2">
            <label for="supplierPhone" class="block text-sm font-semibold text-gray-700"
              >Telefon</label
            >
            <input
              type="text"
              id="supplierPhone"
              v-model="newSupplier.phone"
              placeholder="Telefon eingeben"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            />
          </div>

          <div class="flex justify-end space-x-4 mt-6">
            <button
              type="button"
              @click="closeSupplierModal"
              class="px-4 py-2.5 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors duration-200"
            >
              Abbrechen
            </button>
            <button
              type="submit"
              class="px-4 py-2.5 rounded-xl shadow-md bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-200"
            >
              Speichern
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style scoped></style>
