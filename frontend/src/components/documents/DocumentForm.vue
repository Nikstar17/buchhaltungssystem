<template>
  <div class="flex flex-col h-screen bg-gray-50 text-gray-800">
    <div class="flex overflow-y-auto">
      <!-- Upload Section -->
      <div class="w-3/5 overflow-y-auto">
        <PdfViewer
          ref="pdfViewerRef"
          @file-deleted="deleteFileInfos"
          @file-selected="updateFileUploaded"
        />
      </div>

      <!-- Form Section -->
      <div class="w-2/5 overflow-y-auto">
        <form ref="uploadForm" @submit.prevent="uploadDocument" class="space-y-4">
          <div
            class="flex flex-col mx-auto sticky top-0 z-10 bg-gray-50/95 backdrop-blur-sm py-4 px-6 shadow-sm"
          >
            <div class="flex justify-between items-center mb-2">
              <div class="text-base text-gray-700">
                Netto-Betrag:
                <span class="font-medium">{{ totalNetSum.toFixed(2) }} €</span>
              </div>
              <button
                type="button"
                @click="handleUploadClick"
                class="px-5 py-2.5 rounded-xl shadow-md bg-blue-600 text-white hover:bg-blue-700 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
              >
                Hochladen
              </button>
            </div>
            <div class="text-base text-gray-700">
              Umsatzsteuer: <span class="font-medium">{{ totalTaxSum.toFixed(2) }} €</span>
            </div>
            <div class="text-lg font-semibold text-blue-700 border-t pt-2 mt-1">
              Brutto-Betrag: <span class="font-bold">{{ totalGrossSum.toFixed(2) }} €</span>
            </div>
          </div>
          <div class="bg-white px-6 pb-8 pt-10 space-y-6 !-mt-4 rounded-t-xl shadow-sm">
            <div class="!-mt-4">
              <label class="block text-sm font-semibold text-gray-700 mb-3">Belegart *</label>
              <div class="flex space-x-4">
                <!-- Expense option -->
                <label
                  class="flex-1 flex items-center space-x-3 p-4 border border-gray-300 rounded-xl cursor-pointer transition-all duration-200 hover:bg-blue-50 hover:border-blue-300 focus-within:ring-2 focus-within:ring-blue-500"
                  :class="{
                    'bg-blue-50 border-blue-400 shadow-sm':
                      documentDetails.document_type === 'EXPENSE',
                  }"
                >
                  <input
                    type="radio"
                    value="EXPENSE"
                    v-model="documentDetails.document_type"
                    name="document_type"
                    required
                    class="absolute opacity-0"
                  />
                  <span
                    class="w-5 h-5 flex items-center justify-center border-2 border-gray-400 rounded-full transition-colors duration-200"
                    :class="{ 'border-blue-500': documentDetails.document_type === 'EXPENSE' }"
                  >
                    <span
                      v-if="documentDetails.document_type === 'EXPENSE'"
                      class="w-3 h-3 bg-blue-500 rounded-full animate-scale-in"
                    ></span>
                  </span>
                  <span class="font-medium">Ausgabe</span>
                </label>

                <!-- Income option -->
                <label
                  class="flex-1 flex items-center space-x-3 p-4 border border-gray-300 rounded-xl cursor-pointer transition-all duration-200 hover:bg-blue-50 hover:border-blue-300 focus-within:ring-2 focus-within:ring-blue-500"
                  :class="{
                    'bg-blue-50 border-blue-400 shadow-sm':
                      documentDetails.document_type === 'INCOME',
                  }"
                >
                  <input
                    type="radio"
                    value="INCOME"
                    v-model="documentDetails.document_type"
                    name="document_type"
                    class="absolute opacity-0"
                  />
                  <span
                    class="w-5 h-5 flex items-center justify-center border-2 border-gray-400 rounded-full transition-colors duration-200"
                    :class="{ 'border-blue-500': documentDetails.document_type === 'INCOME' }"
                  >
                    <span
                      v-if="documentDetails.document_type === 'INCOME'"
                      class="w-3 h-3 bg-blue-500 rounded-full animate-scale-in"
                    ></span>
                  </span>
                  <span class="font-medium">Einnahme</span>
                </label>
              </div>
            </div>

            <!-- Document fields -->
            <div class="grid grid-cols-2 gap-5">
              <div class="space-y-2">
                <label for="number" class="block text-sm font-semibold text-gray-700"
                  >Belegnummer *</label
                >
                <input
                  type="text"
                  id="number"
                  v-model="documentDetails.number"
                  required
                  placeholder="Belegnummer eingeben"
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                />
              </div>
              <div class="space-y-2">
                <label for="document_date" class="block text-sm font-semibold text-gray-700"
                  >Belegdatum *</label
                >
                <input
                  type="date"
                  id="document_date"
                  v-model="documentDetails.document_date"
                  required
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-5">
              <div class="space-y-2">
                <label for="supplier_id" class="block text-sm font-semibold text-gray-700">
                  {{ documentDetails.document_type === 'INCOME' ? 'Kunde *' : 'Lieferant *' }}
                </label>
                <select
                  id="supplier_id"
                  v-model="documentDetails.supplier_id"
                  required
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200 bg-white"
                  @change="handleSupplierChange($event)"
                >
                  <option value="" disabled>
                    {{
                      documentDetails.document_type === 'INCOME'
                        ? 'Kunde auswählen'
                        : 'Lieferant auswählen'
                    }}
                  </option>
                  <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">
                    {{ supplier.name }}
                  </option>
                  <option value="add-new-supplier">
                    +
                    {{
                      documentDetails.document_type === 'INCOME'
                        ? 'Kunde hinzufügen'
                        : 'Lieferanten hinzufügen'
                    }}
                  </option>
                </select>
              </div>
              <div class="space-y-2">
                <label for="delivery_date" class="block text-sm font-semibold text-gray-700"
                  >Lieferdatum *</label
                >
                <input
                  type="date"
                  id="delivery_date"
                  v-model="documentDetails.delivery_date"
                  required
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                />
              </div>
            </div>

            <!-- Optional fields -->
            <div v-if="showOptionalFields" class="grid grid-cols-2 gap-5 pt-3 animate-fade-in">
              <div class="space-y-2">
                <label for="link_id" class="block text-sm font-semibold text-gray-700"
                  >Verknüpfung</label
                >
                <input
                  type="text"
                  id="link_id"
                  v-model="documentDetails.link_id"
                  placeholder="link_ids (Coming soon)"
                  disabled
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-300 bg-gray-50 text-gray-500 cursor-not-allowed"
                />
              </div>
              <div class="space-y-2">
                <label for="due_date" class="block text-sm font-semibold text-gray-700"
                  >Fälligkeit</label
                >
                <input
                  type="date"
                  id="due_date"
                  v-model="documentDetails.due_date"
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                />
              </div>
              <div class="space-y-2">
                <label for="cost_center_id" class="block text-sm font-semibold text-gray-700"
                  >Kostenstelle</label
                >
                <input
                  type="text"
                  id="cost_center_id"
                  v-model="documentDetails.cost_center_id"
                  placeholder="cost_center_id (Coming soon)"
                  disabled
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-300 bg-gray-50 text-gray-500 cursor-not-allowed"
                />
              </div>
              <div class="space-y-2">
                <label for="tags" class="block text-sm font-semibold text-gray-700">Tags</label>
                <input
                  type="text"
                  id="tags"
                  v-model="documentDetails.tags"
                  placeholder="Tags eingeben (kommagetrennt)"
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                />
              </div>
            </div>

            <!-- Optional fields toggle -->
            <div class="flex justify-end mb-2">
              <button
                type="button"
                @click="toggleOptionalFields"
                class="text-sm text-blue-600 hover:text-blue-800 transition-colors duration-200 flex items-center"
              >
                <span>{{
                  showOptionalFields ? 'Optionale Felder ausblenden' : 'Optionale Felder anzeigen'
                }}</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4 ml-1 transition-transform duration-200"
                  :class="showOptionalFields ? 'rotate-180' : ''"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>
            </div>

            <!-- Positions -->
            <div
              v-for="(position, index) in positions"
              :key="index"
              class="mb-6 p-5 border border-gray-200 rounded-xl bg-gray-50/50 shadow-sm transition-all duration-200 hover:border-gray-300"
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-medium text-gray-800 text-lg flex items-center">
                  <span
                    class="bg-blue-100 text-blue-800 rounded-full h-6 w-6 flex items-center justify-center mr-2 text-sm"
                  >
                    {{ index + 1 }}
                  </span>
                  Position {{ index + 1 }}
                </h3>
                <button
                  v-if="index > 0"
                  type="button"
                  @click="removePosition(index)"
                  class="text-sm text-red-600 hover:text-red-800 transition-colors duration-200 flex items-center"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4 mr-1"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                  Position entfernen
                </button>
              </div>
              <div class="grid grid-cols-2 gap-5">
                <div class="space-y-2">
                  <label
                    :for="'description-' + index"
                    class="block text-sm font-semibold text-gray-700"
                    >Beschreibung *</label
                  >
                  <input
                    type="text"
                    :id="'description-' + index"
                    v-model="position.description"
                    required
                    placeholder="Beschreibung eingeben"
                    class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                  />
                </div>
                <div class="space-y-2">
                  <label
                    :for="'category_name-' + index"
                    class="block text-sm font-semibold text-gray-700"
                    >Kategorie</label
                  >
                  <input
                    type="text"
                    :id="'category_name-' + index"
                    v-model="position.category_id"
                    placeholder="Kategorie eingeben (z.B. Miete)"
                    class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                  />
                </div>
                <div class="space-y-2">
                  <label
                    :for="'umsatzsteuer-' + index"
                    class="block text-sm font-semibold text-gray-700"
                    >Umsatzsteuer *</label
                  >
                  <select
                    :id="'umsatzsteuer-' + index"
                    v-model="position.tax_rate_id"
                    required
                    class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200 bg-white"
                    @change="handleTaxRateChange($event, index)"
                  >
                    <option value="" disabled>Umsatzsteuer auswählen</option>
                    <option v-for="rate in taxRates" :key="rate.id" :value="rate.id">
                      {{ rate.name }}
                    </option>
                    <option value="add-new-taxrate">+ Steuerregel hinzufügen</option>
                  </select>
                </div>
                <div class="space-y-2">
                  <label :for="'menge-' + index" class="block text-sm font-semibold text-gray-700"
                    >Menge *</label
                  >
                  <input
                    type="number"
                    :id="'menge-' + index"
                    v-model.number="position.quantity"
                    required
                    step="1"
                    min="0"
                    placeholder="Menge"
                    class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                  />
                </div>
                <div class="space-y-2">
                  <label
                    :for="'einzelpreis-' + index"
                    class="block text-sm font-semibold text-gray-700"
                    >Einzelpreis *</label
                  >
                  <input
                    type="number"
                    :id="'einzelpreis-' + index"
                    v-model.number="position.unit_price"
                    required
                    step="0.01"
                    placeholder="Einzelpreis"
                    class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
                  />
                </div>
                <div class="space-y-2">
                  <label
                    :for="'price-type-' + index"
                    class="block text-sm font-semibold text-gray-700"
                    >Preistyp</label
                  >
                  <div class="flex space-x-4">
                    <label class="flex items-center">
                      <input
                        type="radio"
                        :name="'price-type-' + index"
                        :value="true"
                        v-model="position.is_gross_price"
                        class="mr-2"
                      />
                      <span>Brutto</span>
                    </label>
                    <label class="flex items-center">
                      <input
                        type="radio"
                        :name="'price-type-' + index"
                        :value="false"
                        v-model="position.is_gross_price"
                        class="mr-2"
                      />
                      <span>Netto</span>
                    </label>
                  </div>
                </div>
                <div class="space-y-2">
                  <label class="block text-sm font-semibold text-gray-700">Gesamtpreis</label>
                  <input
                    type="text"
                    name="total_price"
                    :value="getPositionTotal(position).toFixed(2)"
                    class="w-full px-4 py-2.5 rounded-lg border border-gray-300 bg-gray-100 font-medium text-blue-700"
                    disabled
                  />
                </div>
              </div>
            </div>

            <!-- Add Position button -->
            <div class="flex justify-center pt-3">
              <button
                type="button"
                @click="addPosition"
                class="px-4 py-2 rounded-lg border border-blue-200 bg-blue-50 text-blue-700 hover:bg-blue-100 transition-colors duration-200 flex items-center"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 mr-1"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
                Position hinzufügen
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Modal für neue Steuerregel -->
  <div
    v-if="showTaxRateModal"
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in"
  >
    <div class="bg-white p-6 rounded-xl shadow-lg w-1/3 max-w-md animate-scale-in">
      <h2 class="text-lg font-bold mb-4 text-gray-800">Neue Steuerregel hinzufügen</h2>
      <form @submit.prevent="addNewTaxRate">
        <div class="mb-4 space-y-2">
          <label for="taxRateName" class="block text-sm font-semibold text-gray-700"
            >Name der Steuerregel</label
          >
          <input
            type="text"
            id="taxRateName"
            v-model="newTaxRate.name"
            required
            placeholder='z.B. "USt 19%"'
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>
        <div class="mb-4 space-y-2">
          <label for="taxRatePercentage" class="block text-sm font-semibold text-gray-700"
            >Steuersatz (%)</label
          >
          <input
            type="number"
            id="taxRatePercentage"
            v-model.number="newTaxRate.percentage"
            required
            step="0.01"
            placeholder="Steuersatz eingeben"
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>
        <div class="mb-4 space-y-2">
          <label for="taxRateValidForm" class="block text-sm font-semibold text-gray-700"
            >Gültig ab</label
          >
          <input
            type="date"
            id="taxRateValidForm"
            v-model="newTaxRate.valid_from"
            required
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>
        <div class="flex justify-end space-x-4 mt-6">
          <button
            type="button"
            @click="closeTaxRateModal"
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
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import API_URL from '@/api';
import PdfViewer from '../common/PdfViewer.vue';
import { showSnackbarMessage } from '@/composables/useSnackbar';
import { SupplierService, TaxRateService } from '@/services';

const pdfViewerRef = ref(null); // Referenz auf den PdfViewer

// Formular-Referenzen
const uploadForm = ref(null); // Referenz auf das Upload-Formular

// Reaktive Zustände für die Belegarten und Dokumentdaten
const suppliers = ref([]); // Optionen für das Lieferanten-Dropdown
const positions = ref([
  {
    line_number: '',
    description: '',
    quantity: '',
    unit_price: '',
    total_price: '',
    category_id: '',
    tax_rate_id: '',
    account_id: '',
    is_gross_price: true, // Standard: Brutto-Eingabe
  },
]);

// Reaktive Zustände für Umsatzsteuer
const taxRates = ref([]); // Optionen für das Umsatzsteuer-Dropdown
const newTaxRate = ref({ name: '', percentage: '', valid_from: '' }); // Neue Umsatzsteuer-Daten

// Modal- und Dateizustände
const showTaxRateModal = ref(false); // Zeigt das Modal für neue Umsatzsteuer an
const showSupplierModal = ref(false);
const isFileUploaded = ref(false); // Prüft, ob ein Dokument hochgeladen wurde

// Temporäre Datei
const tempFile = ref(null);

// Reaktive Zustände für Dokumenteninformationen
const documentDetails = ref({
  document_type: '',
  status: 'OPEN',
  number: '',
  document_date: '',
  supplier_id: '',
  delivery_date: '',
  link_id: '', // TODO: Implement Links
  due_date: '',
  cost_center_id: '',
  currency_code: 'EUR', // TODO: Add dynamic currency selection in the future
  line_number: '',
  description: '',
  quantity: '',
  unit_price: '',
  total_price: '',
  category_id: '',
  tax_rate_id: '',
  account_id: '',
  filename: '',
  file_path: '',
  mimetype: '',
  file_size: '',
});

const newSupplier = ref({
  name: '',
  address: '',
  tax_number: '',
  vat_id: '',
  iban: '',
  bic: '',
  email: '',
  phone: '',
}); // Neue Lieferantendaten

const addPosition = () => {
  positions.value.push({
    line_number: '',
    description: '',
    quantity: '',
    unit_price: '',
    total_price: '',
    category_id: '',
    tax_rate_id: '',
    account_id: '',
    is_gross_price: true, // Standard: Brutto-Eingabe
  });

  // Nach dem Hinzufügen zum neuen Element scrollen
  setTimeout(() => {
    const positionElements = document.querySelectorAll('.p-5.border.border-gray-200.rounded-xl');
    if (positionElements.length > 0) {
      const newPositionElement = positionElements[positionElements.length - 1];
      if (newPositionElement) {
        newPositionElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }, 50);
};

const removePosition = (index) => {
  if (index > 0) {
    positions.value.splice(index, 1);
  }
};

const handleTaxRateChange = (event, index) => {
  if (event.target.value === 'add-new-taxrate') {
    showTaxRateModal.value = true;
    event.target.value = ''; // Reset the selection
  }
};

const handleSupplierChange = (event) => {
  if (event.target.value === 'add-new-supplier') {
    showSupplierModal.value = true;
    event.target.value = ''; // Reset the selection
  }
};

const closeTaxRateModal = () => {
  showTaxRateModal.value = false;
  newTaxRate.value = { name: '', percentage: '', valid_from: '' };
  documentDetails.value.tax_rate_id = ''; // Reset the dropdown value for the main form

  // Reset the dropdown value for all positions
  positions.value.forEach((position) => {
    if (position.tax_rate_id === 'add-new-taxrate') {
      position.tax_rate_id = '';
    }
  });
};

const closeSupplierModal = () => {
  showSupplierModal.value = false;
  newSupplier.value = { name: '', address: '' };
  documentDetails.value.supplier_id = ''; // Reset the dropdown value
};

const getTaxRates = async () => {
  try {
    taxRates.value = await TaxRateService.getTaxRates();
  } catch (error) {
    console.error('Fehler beim Abrufen der Taxrates');
  }
};

const getSuppliers = async () => {
  try {
    suppliers.value = await SupplierService.getSuppliers();
  } catch (error) {
    console.error('Fehler beim Abrufen der Lieferanten');
  }
};

const addNewTaxRate = async () => {
  try {
    // Use TaxRateService to create a new tax rate
    const createdTaxRate = await TaxRateService.createTaxRate(newTaxRate.value);

    // Refresh tax rates and close modal
    await getTaxRates();
    closeTaxRateModal();

    showSnackbarMessage('Steuerregel erfolgreich hinzugefügt', 'success');
  } catch (error) {
    console.error('Fehler beim Hinzufügen der Steuerregel:', error);
    showSnackbarMessage('Fehler beim Hinzufügen der Steuerregel', 'error');
  }
};

const addNewSupplier = async () => {
  try {
    const csrfToken = document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrf_access_token='))
      ?.split('=')[1];

    const response = await fetch(`${API_URL}/api/suppliers`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': csrfToken,
      },
      body: JSON.stringify(newSupplier.value),
    });

    if (response.ok) {
      const createdSupplier = await response.json();
      suppliers.value.push(createdSupplier);
      fetchSuppliers();
      closeSupplierModal();
    } else {
      console.error('Fehler beim Hinzufügen des Lieferanten');
    }
  } catch (error) {
    console.error('API-Fehler:', error);
  }
};

const handleUploadClick = () => {
  const form = uploadForm.value;

  if (!form.reportValidity()) {
    return;
  }

  if (!isFileUploaded.value) {
    showSnackbarMessage('Bitte laden Sie zuerst eine Datei hoch');
    return;
  }

  uploadDocument();

  // Aufruf der deleteFile-Methode in PdfViewer
  pdfViewerRef.value?.deleteFile();
};

const updateFileUploaded = (fileDetails) => {
  tempFile.value = fileDetails; // Temporäre Datei speichern
  isFileUploaded.value = true;

  documentDetails.value.filename = fileDetails.name;
  documentDetails.value.mimetype = fileDetails.type;
  documentDetails.value.file_size = fileDetails.size;
};

const uploadDocument = async () => {
  const formData = new FormData();

  // Füge die allgemeinen Dokumentdetails hinzu
  formData.append('document_type', documentDetails.value.document_type);
  formData.append('status', documentDetails.value.status);
  formData.append('number', documentDetails.value.number);
  formData.append('document_date', documentDetails.value.document_date);
  formData.append('supplier_id', documentDetails.value.supplier_id);
  formData.append('delivery_date', documentDetails.value.delivery_date);
  formData.append('link_id', documentDetails.value.link_id);
  formData.append('due_date', documentDetails.value.due_date);
  formData.append('cost_center_id', documentDetails.value.cost_center_id);
  formData.append('currency_code', documentDetails.value.currency_code);

  // Füge die Datei hinzu
  if (tempFile.value) {
    formData.append('file', tempFile.value); // Datei an formData anhängen
  }

  const positionsWithLineNumbers = positions.value.map((position, index) => {
    // Berechne den korrekten Einheitspreis je nach Brutto/Netto-Einstellung
    let unitPrice = Number(position.unit_price) || 0;
    let totalPrice = (position.quantity || 0) * unitPrice;

    // Zusätzliche Informationen zu Brutto/Netto-Einstellung
    return {
      line_number: index + 1,
      description: position.description,
      quantity: position.quantity || 0,
      unit_price: unitPrice,
      total_price: totalPrice,
      category_id: position.category_id || null,
      tax_rate_id: position.tax_rate_id || null,
      account_id: position.account_id || null,
      is_gross_price: position.is_gross_price,
    };
  });
  formData.append('positions', JSON.stringify(positionsWithLineNumbers));

  try {
    const csrfToken = document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrf_access_token='))
      ?.split('=')[1];

    const response = await fetch(`${API_URL}/api/documents`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRF-TOKEN': csrfToken,
      },
      body: formData,
    });

    if (response.ok) {
      resetForm();
      showSnackbarMessage('Beleg erfolgreich hochgeladen!', 'success');
    } else {
      showSnackbarMessage('Fehler beim Hochladen des Belegs', 'error');
    }
  } catch (error) {
    console.error('Beleg-Upload-Fehler:', error);
    showSnackbarMessage('Ein unerwarteter Fehler ist aufgetreten.', 'error');
  }
};

const resetForm = () => {
  documentDetails.value = {
    document_type: '',
    status: 'OPEN',
    number: '',
    document_date: '',
    supplier_id: '',
    delivery_date: '',
    link_id: '',
    due_date: '',
    cost_center_id: '',
    currency_code: 'EUR',
    filename: '',
    file_path: '',
    mimetype: '',
    file_size: '',
  };
  positions.value = [
    {
      description: '',
      quantity: '',
      unit_price: '',
      total_price: '',
      category_id: '',
      tax_rate_id: '',
      account_id: '',
      is_gross_price: true, // Standard: Brutto-Eingabe
    },
  ];
};

const deleteFileInfos = () => {
  tempFile.value = null; // Temporäre Datei zurücksetzen
  isFileUploaded.value = false;
  documentDetails.value.filename = '';
  documentDetails.value.mimetype = '';
  documentDetails.value.file_size = '';
};

const showOptionalFields = ref(false);

const toggleOptionalFields = () => {
  showOptionalFields.value = !showOptionalFields.value;
};

// Berechnete Eigenschaft für den Gesamtbetrag jeder Position
const getPositionTotal = (position) => {
  const quantity = Number(position.quantity) || 0;
  const unitPrice = Number(position.unit_price) || 0;
  const total = quantity * unitPrice;
  return total;
};

// Berechnete Eigenschaft für den Bruttobetrag
const totalGrossSum = computed(() => {
  return positions.value.reduce((sum, position) => {
    // Wenn der Preis bereits Brutto ist, verwenden wir ihn direkt
    if (position.is_gross_price) {
      return sum + getPositionTotal(position);
    }
    // Wenn der Preis Netto ist, berechnen wir den Bruttobetrag
    else {
      const total = getPositionTotal(position);
      const taxRate = taxRates.value.find((rate) => rate.id === position.tax_rate_id);
      const taxPercentage = taxRate ? Number(taxRate.percentage) / 100 : 0;
      return sum + total * (1 + taxPercentage);
    }
  }, 0);
});

// Berechnete Eigenschaft für die Summe der Umsatzsteuer
const totalTaxSum = computed(() => {
  return positions.value.reduce((sum, position) => {
    const quantity = Number(position.quantity) || 0;
    const unitPrice = Number(position.unit_price) || 0;
    const total = quantity * unitPrice;

    // Finde den passenden Steuersatz für diese Position
    const taxRate = taxRates.value.find((rate) => rate.id === position.tax_rate_id);
    const taxPercentage = taxRate ? Number(taxRate.percentage) / 100 : 0;

    if (position.is_gross_price) {
      // Berechnung der USt aus Bruttobetrag: Brutto * (Steuersatz / (100 + Steuersatz))
      const taxAmount = total * (taxPercentage / (1 + taxPercentage));
      return sum + taxAmount;
    } else {
      // Berechnung der USt aus Nettobetrag: Netto * Steuersatz
      const taxAmount = total * taxPercentage;
      return sum + taxAmount;
    }
  }, 0);
});

// Berechnete Eigenschaft für den Nettobetrag
const totalNetSum = computed(() => {
  return positions.value.reduce((sum, position) => {
    const quantity = Number(position.quantity) || 0;
    const unitPrice = Number(position.unit_price) || 0;
    const total = quantity * unitPrice;

    if (position.is_gross_price) {
      // Berechnung des Nettobetrags aus Bruttobetrag
      const taxRate = taxRates.value.find((rate) => rate.id === position.tax_rate_id);
      const taxPercentage = taxRate ? Number(taxRate.percentage) / 100 : 0;
      const netAmount = total / (1 + taxPercentage);
      return sum + netAmount;
    } else {
      // Bei Nettobetrag direkt verwenden
      return sum + total;
    }
  }, 0);
});

onMounted(() => {
  getTaxRates();
  getSuppliers();
});
</script>

<style scoped>
.animate-scale-in {
  animation: scaleIn 0.2s ease-out forwards;
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-out forwards;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
