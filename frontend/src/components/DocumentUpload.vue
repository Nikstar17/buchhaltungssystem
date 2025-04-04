<template>
  <div class="flex flex-col max-h-screen bg-gray-50 text-gray-800">
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
          <div class="flex justify-end mr-2 mx-auto sticky top-0 z-10 bg-gray-50 py-5">
            <button
              type="button"
              @click="handleUploadClick"
              class="px-4 py-2 rounded-xl shadow bg-blue-600 text-white hover:bg-blue-700"
            >
              Hochladen
            </button>
          </div>
          <div class="bg-white px-5 pb-5 pt-12 space-y-4 !-mt-4">
            <div class="!-mt-4">
              <label class="block text-sm font-semibold text-gray-700 mb-1">Belegart *</label>
              <div class="flex space-x-4">
                <label
                  class="flex items-center space-x-2 p-3 border border-gray-300 rounded-xl cursor-pointer transition hover:bg-blue-50 focus-within:ring-2 focus-within:ring-blue-500"
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
                    class="w-4 h-4 flex items-center justify-center border-2 border-gray-400 rounded-full"
                  >
                    <span
                      v-if="documentDetails.document_type === 'EXPENSE'"
                      class="w-2 h-2 bg-blue-500 rounded-full"
                    ></span>
                  </span>
                  <span class="font-medium">Ausgabe</span>
                </label>
                <label
                  class="flex items-center space-x-2 p-3 border border-gray-300 rounded-xl cursor-pointer transition hover:bg-blue-50 focus-within:ring-2 focus-within:ring-blue-500"
                >
                  <input
                    type="radio"
                    value="INCOME"
                    v-model="documentDetails.document_type"
                    name="document_type"
                    class="absolute opacity-0"
                  />
                  <span
                    class="w-4 h-4 flex items-center justify-center border-2 border-gray-400 rounded-full"
                  >
                    <span
                      v-if="documentDetails.document_type === 'INCOME'"
                      class="w-2 h-2 bg-blue-500 rounded-full"
                    ></span>
                  </span>
                  <span class="font-medium">Einnahme</span>
                </label>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="number" class="block text-sm font-semibold text-gray-700 mb-1"
                  >Belegnummer *</label
                >
                <input
                  type="text"
                  id="number"
                  v-model="documentDetails.number"
                  required
                  placeholder="Belegnummer eingeben"
                  class="w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label for="document_date" class="block text-sm font-semibold text-gray-700 mb-1"
                  >Belegdatum *</label
                >
                <input
                  type="date"
                  id="document_date"
                  v-model="documentDetails.document_date"
                  required
                  class="w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="supplier_id" class="block font-medium">
                  {{ documentDetails.document_type === 'INCOME' ? 'Kunde *' : 'Lieferant *' }}
                </label>
                <select
                  id="supplier_id"
                  v-model="documentDetails.supplier_id"
                  required
                  class="border border-gray-300 rounded px-3 py-2 w-full"
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
              <div>
                <label for="delivery_date" class="block font-medium">Lieferdatum *</label>
                <input
                  type="date"
                  id="delivery_date"
                  v-model="documentDetails.delivery_date"
                  required
                  class="border border-gray-300 rounded px-3 py-2 w-full"
                />
              </div>
            </div>

            <!-- Optionalen Felder -->
            <div v-if="showOptionalFields" class="grid grid-cols-2 gap-4">
              <div>
                <label for="link_id" class="block font-medium">Verknüpfung</label>
                <input
                  type="text"
                  id="link_id"
                  v-model="documentDetails.link_id"
                  placeholder="link_ids (Coming soon)"
                  disabled
                  class="border border-gray-300 rounded px-3 py-2 w-full"
                />
              </div>
              <div>
                <label for="due_date" class="block font-medium">Fälligkeit</label>
                <input
                  type="date"
                  id="due_date"
                  v-model="documentDetails.due_date"
                  class="border border-gray-300 rounded px-3 py-2 w-full"
                />
              </div>
              <div>
                <label for="cost_center_id" class="block font-medium">Kostenstelle</label>
                <input
                  type="text"
                  id="cost_center_id"
                  v-model="documentDetails.cost_center_id"
                  placeholder="cost_center_id (Coming soon)"
                  disabled
                  class="border border-gray-300 rounded px-3 py-2 w-full"
                />
              </div>
              <div>
                <label for="tags" class="block font-medium">Tags</label>
                <input
                  type="text"
                  id="tags"
                  v-model="documentDetails.tags"
                  placeholder="Tags eingeben (kommagetrennt)"
                  class="border border-gray-300 rounded px-3 py-2 w-full"
                />
              </div>
            </div>

            <!-- Optionalen Felder Button -->
            <div class="flex justify-end mb-4">
              <button
                type="button"
                @click="toggleOptionalFields"
                class="text-sm text-blue-600 hover:underline"
              >
                {{
                  showOptionalFields ? 'Optionale Felder ausblenden' : 'Optionale Felder anzeigen'
                }}
              </button>
            </div>
            <br />

            <!-- Positionen -->
            <div v-for="(position, index) in positions" :key="index" class="mb-6">
              <div class="flex items-center my-4">
                <div class="flex-grow border-t border-black"></div>
                <span class="mx-4 font-sans text-lg">Position {{ index + 1 }}</span>
                <div class="flex-grow border-t border-black"></div>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label :for="'description-' + index" class="block font-medium"
                    >Beschreibung *</label
                  >
                  <input
                    type="text"
                    :id="'description-' + index"
                    v-model="position.description"
                    required
                    placeholder="Beschreibung eingeben"
                    class="border border-gray-300 rounded px-3 py-2 w-full"
                  />
                </div>
                <div>
                  <label :for="'category_name-' + index" class="block font-medium">Kategorie</label>
                  <input
                    type="text"
                    :id="'category_name-' + index"
                    v-model="position.category_id"
                    placeholder="Kategorie eingeben (z.B. Miete)"
                    class="border border-gray-300 rounded px-3 py-2 w-full"
                  />
                </div>
                <div>
                  <label :for="'umsatzsteuer-' + index" class="block font-medium"
                    >Umsatzsteuer *</label
                  >
                  <select
                    :id="'umsatzsteuer-' + index"
                    v-model="position.tax_rate_id"
                    required
                    class="border border-gray-300 rounded px-3 py-2 w-full"
                    @change="handleTaxRateChange($event, index)"
                  >
                    <option value="" disabled>Umsatzsteuer auswählen</option>
                    <option v-for="rate in taxRates" :key="rate.id" :value="rate.id">
                      {{ rate.name }}
                    </option>
                    <option value="add-new-taxrate">+ Steuerregel hinzufügen</option>
                  </select>
                </div>
                <div>
                  <label :for="'menge-' + index" class="block font-medium">Menge *</label>
                  <input
                    type="number"
                    :id="'menge-' + index"
                    v-model.number="position.quantity"
                    required
                    step="1"
                    min="0"
                    placeholder="Menge"
                    class="border border-gray-300 rounded px-3 py-2 w-full"
                  />
                </div>
                <div>
                  <label :for="'einzelpreis-' + index" class="block font-medium"
                    >Einzelpreis *</label
                  >
                  <input
                    type="number"
                    :id="'einzelpreis-' + index"
                    v-model.number="position.unit_price"
                    required
                    step="0.01"
                    placeholder="Einzelpreis"
                    class="border border-gray-300 rounded px-3 py-2 w-full"
                  />
                </div>
                <div>
                  <label class="block font-medium">Gesamtpreis</label>
                  <input
                    type="number"
                    name="total_price"
                    :value="(position.quantity || 0) * (position.unit_price || 0)"
                    class="border border-gray-300 rounded px-3 py-2 w-full bg-gray-100"
                    disabled
                  />
                </div>
                <button
                  v-if="index > 0"
                  type="button"
                  @click="removePosition(index)"
                  class="text-sm text-red-600 hover:underline col-span-2"
                >
                  Position entfernen
                </button>
              </div>
            </div>

            <!-- Buttons new Position and Upload -->
            <div class="flex justify-between">
              <button
                type="button"
                @click="addPosition"
                class="text-sm font-medium text-blue-600 hover:text-blue-800 transition"
              >
                + Position hinzufügen
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Snackbar -->
  <div
    v-if="showSnackbar"
    :class="snackbarType === 'success' ? 'bg-green-600/90' : 'bg-red-600/90'"
    class="fixed top-4 left-1/2 transform -translate-x-1/2 text-white px-6 py-3 rounded-xl shadow-lg transition-all duration-300"
  >
    {{ snackbarMessage }}
  </div>

  <!-- Modal für neue Steuerregel -->
  <div
    v-if="showTaxRateModal"
    class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-xl shadow-lg w-1/3">
      <h2 class="text-lg font-bold mb-4">Neue Steuerregel hinzufügen</h2>
      <form @submit.prevent="addNewTaxRate">
        <div class="mb-4">
          <label for="taxRateName" class="block text-sm font-semibold text-gray-700 mb-1"
            >Name der Steuerregel</label
          >
          <input
            type="text"
            id="taxRateName"
            v-model="newTaxRate.name"
            required
            placeholder='z.B. "USt 19%"'
            class="w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div class="mb-4">
          <label for="taxRatePercentage" class="block font-medium">Steuersatz (%)</label>
          <input
            type="number"
            id="taxRatePercentage"
            v-model.number="newTaxRate.percentage"
            required
            step="0.01"
            placeholder="Steuersatz eingeben"
            class="border border-gray-300 rounded px-3 py-2 w-full"
          />
        </div>
        <div class="mb-4">
          <label for="taxRateValidForm" class="block font-medium">Gültig ab</label>
          <input
            type="date"
            id="taxRateValidForm"
            v-model="newTaxRate.valid_from"
            required
            class="border border-gray-300 rounded px-3 py-2 w-full"
          />
        </div>
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="closeTaxRateModal"
            class="px-4 py-2 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition"
          >
            Abbrechen
          </button>
          <button
            type="submit"
            class="px-4 py-2 rounded-xl shadow bg-blue-600 text-white hover:bg-blue-700 transition"
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
    class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-xl shadow-lg w-1/3">
      <h2 class="text-lg font-bold mb-4">Neuen Lieferanten hinzufügen</h2>
      <form @submit.prevent="addNewSupplier">
        <div class="mb-4">
          <label for="supplierName" class="block text-sm font-semibold text-gray-700 mb-1"
            >Name des Lieferanten *</label
          >
          <input
            type="text"
            id="supplierName"
            v-model="newSupplier.name"
            required
            placeholder="Lieferantenname eingeben"
            class="w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="mb-4">
          <label for="supplierAddress" class="block font-medium">Adresse *</label>
          <input
            type="text"
            id="supplierAddress"
            v-model="newSupplier.address"
            required
            placeholder="Adresse eingeben"
            class="border border-gray-300 rounded px-3 py-2 w-full"
          />
        </div>

        <div class="mb-4">
          <label for="supplierTaxnumber" class="block font-medium">Steuernummer</label>
          <input
            type="text"
            id="supplierTaxnumber"
            v-model="newSupplier.tax_number"
            placeholder="Steuernummer eingeben"
            class="border border-gray-300 rounded px-3 py-2 w-full"
          />
        </div>

        <div class="mb-4">
          <label for="supplierVatId" class="block font-medium">USt-IdNr.</label>
          <input
            type="text"
            id="supplierVatId"
            v-model="newSupplier.vat_id"
            placeholder="USt-IdNr. eingeben"
            class="border border-gray-300 rounded px-3 py-2 w-full"
          />
        </div>

        <div class="mb-4">
          <label for="supplierIban" class="block font-medium">IBAN</label>
          <input
            type="text"
            id="supplierIban"
            v-model="newSupplier.iban"
            placeholder="IBAN eingeben"
            class="border border-gray-300 rounded px-3 py-2 w-full"
          />
        </div>

        <div class="mb-4">
          <label for="supplierBic" class="block font-medium">BIC</label>
          <input
            type="text"
            id="supplierBic"
            v-model="newSupplier.bic"
            placeholder="BIC eingeben"
            class="border border-gray-300 rounded px-3 py-2 w-full"
          />
        </div>

        <div class="mb-4">
          <label for="supplierEmail" class="block font-medium">E-Mail</label>
          <input
            type="text"
            id="supplierEmail"
            v-model="newSupplier.email"
            placeholder="E-Mail eingeben"
            class="border border-gray-300 rounded px-3 py-2 w-full"
          />
        </div>

        <div class="mb-4">
          <label for="supplierPhone" class="block font-medium">Telefon</label>
          <input
            type="text"
            id="supplierPhone"
            v-model="newSupplier.phone"
            placeholder="Telefon eingeben"
            class="border border-gray-300 rounded px-3 py-2 w-full"
          />
        </div>

        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="closeSupplierModal"
            class="px-4 py-2 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition"
          >
            Abbrechen
          </button>
          <button
            type="submit"
            class="px-4 py-2 rounded-xl shadow bg-blue-600 text-white hover:bg-blue-700 transition"
          >
            Speichern
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import API_URL from '@/api';
import PdfViewer from './PdfViewer.vue';
import {
  showSnackbar,
  snackbarMessage,
  snackbarType,
  showSnackbarMessage,
} from '@/composables/useSnackbar';

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
  });
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
  newTaxRate.value = { name: '', value: '' };
};

const closeSupplierModal = () => {
  showSupplierModal.value = false;
  newSupplier.value = { name: '', address: '' };
};

const fetchTaxRates = async () => {
  try {
    const response = await fetch(`${API_URL}/api/tax_rates`, {
      method: 'GET',
      credentials: 'include',
    });

    if (response.ok) {
      taxRates.value = await response.json();
    } else {
      console.error('Fehler beim Abrufen der Umsatzsteuersätze');
    }
  } catch (error) {
    console.error('API-Fehler:', error);
  }
};

const fetchSuppliers = async () => {
  try {
    const response = await fetch(`${API_URL}/api/suppliers`, {
      method: 'GET',
      credentials: 'include',
    });

    if (response.ok) {
      suppliers.value = await response.json();
    } else {
      console.error('Fehler beim Abrufen der Lieferanten');
    }
  } catch (error) {
    console.error('API-Fehler:', error);
  }
};

const addNewTaxRate = async () => {
  try {
    const csrfToken = document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrf_access_token='))
      ?.split('=')[1];

    const response = await fetch(`${API_URL}/api/tax_rates`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': csrfToken,
      },
      body: JSON.stringify(newTaxRate.value),
    });

    if (response.ok) {
      const createdTaxRate = await response.json();
      taxRates.value.push(createdTaxRate);
      fetchTaxRates();
      closeTaxRateModal();
    } else {
      console.error('Fehler beim Hinzufügen der Steuerregel');
    }
  } catch (error) {
    console.error('API-Fehler:', error);
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

  const positionsWithLineNumbers = positions.value.map((position, index) => ({
    line_number: index + 1,
    description: position.description,
    quantity: position.quantity || 0,
    unit_price: position.unit_price || 0,
    total_price: (position.quantity || 0) * (position.unit_price || 0),
    category_id: position.category_id || null,
    tax_rate_id: position.tax_rate_id || null,
    account_id: position.account_id || null,
  }));
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

onMounted(() => {
  fetchTaxRates();
  fetchSuppliers();
});
</script>

<style scoped></style>
