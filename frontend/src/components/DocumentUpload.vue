<template>
  <div class="flex space-x-4 max-h-screen p-5">
    <div class="w-3/5 overflow-y-auto">
      <PdfViewer @file-selected="updateFileUploaded" />
    </div>

    <!-- Form Section -->
    <div class="w-2/5 overflow-y-auto">
      <form ref="uploadForm" @submit.prevent="uploadDocument" class="space-y-4">
        <div>
          <label class="block font-medium">Belegart *</label>
          <div class="flex space-x-4">
            <label
              class="flex items-center space-x-2 p-2 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-100 focus-within:ring-2 focus-within:ring-blue-500"
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
              class="flex items-center space-x-2 p-2 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-100 focus-within:ring-2 focus-within:ring-blue-500"
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
            <label for="number" class="block font-medium">Belegnummer *</label>
            <input
              type="text"
              id="number"
              v-model="documentDetails.number"
              required
              placeholder="Belegnummer eingeben"
              class="border border-gray-300 rounded px-3 py-2 w-full focus:invalid:border-red-500"
            />
          </div>
          <div>
            <label for="document_date" class="block font-medium">Belegdatum *</label>
            <input
              type="date"
              id="document_date"
              v-model="documentDetails.document_date"
              required
              class="border border-gray-300 rounded px-3 py-2 w-full"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="supplier_id" class="block font-medium">Lieferant *</label>
            <select
              id="supplier_id"
              v-model="documentDetails.supplier_id"
              required
              class="border border-gray-300 rounded px-3 py-2 w-full"
              @change="handleSupplierChange($event)"
            >
              <option value="" disabled>Lieferant auswählen</option>
              <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">
                {{ supplier.name }}
              </option>
              <option value="add-new-supplier">+ Lieferanten hinzufügen</option>
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

        <div class="grid grid-cols-2 gap-4">
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
        </div>

        <div class="grid grid-cols-2 gap-4">
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
        <br />
        <div v-for="(position, index) in positions" :key="index" class="mb-6">
          <div class="flex items-center my-4">
            <div class="flex-grow border-t border-black"></div>
            <span class="mx-4 font-sans text-lg">Position {{ index + 1 }}</span>
            <div class="flex-grow border-t border-black"></div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label :for="'description-' + index" class="block font-medium">Beschreibung *</label>
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
                v-model="position.categoryName"
                placeholder="Kategorie eingeben (z.B. Miete)"
                class="border border-gray-300 rounded px-3 py-2 w-full"
              />
            </div>
            <div>
              <label :for="'umsatzsteuer-' + index" class="block font-medium">Umsatzsteuer *</label>
              <select
                :id="'umsatzsteuer-' + index"
                v-model="position.umsatzsteuer"
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
                v-model.number="position.menge"
                required
                step="1"
                min="0"
                placeholder="Menge"
                class="border border-gray-300 rounded px-3 py-2 w-full"
              />
            </div>
            <div>
              <label :for="'einzelpreis-' + index" class="block font-medium">Einzelpreis *</label>
              <input
                type="number"
                :id="'einzelpreis-' + index"
                v-model.number="position.einzelpreis"
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
                :value="(position.menge || 0) * (position.einzelpreis || 0)"
                class="border border-gray-300 rounded px-3 py-2 w-full bg-gray-100"
                disabled
              />
            </div>
            <button
              v-if="index > 0"
              type="button"
              @click="removePosition(index)"
              class="col-span-2 bg-gray-200 text-red-700 px-4 py-2 rounded hover:bg-gray-300"
            >
              Position entfernen
            </button>
          </div>
        </div>

        <div class="flex justify-between">
          <button
            type="button"
            @click="addPosition"
            class="bg-gray-200 text-gray-700 px-4 py-2 rounded shadow hover:bg-gray-300"
          >
            Position hinzufügen
          </button>
          <button
            type="button"
            @click="handleUploadClick"
            class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700"
          >
            Hochladen
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Snackbar -->
  <div
    v-if="showSnackbar"
    :class="snackbarType === 'success' ? 'bg-green-700' : 'bg-red-700'"
    class="fixed top-4 left-1/2 transform -translate-x-1/2 text-white px-4 py-2 rounded shadow-lg transition-opacity duration-300"
  >
    {{ snackbarMessage }}
  </div>

  <!-- Modal für neue Steuerregel -->
  <div
    v-if="showTaxRateModal"
    class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded shadow-lg w-1/3">
      <h2 class="text-lg font-bold mb-4">Neue Steuerregel hinzufügen</h2>
      <form @submit.prevent="addNewTaxRate">
        <div class="mb-4">
          <label for="taxRateName" class="block font-medium">Name der Steuerregel</label>
          <input
            type="text"
            id="taxRateName"
            v-model="newTaxRate.name"
            required
            placeholder='z.B. "USt 19%"'
            class="border border-gray-300 rounded px-3 py-2 w-full"
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
            class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
          >
            Abbrechen
          </button>
          <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
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
    <div class="bg-white p-6 rounded shadow-lg w-1/3">
      <h2 class="text-lg font-bold mb-4">Neuen Lieferanten hinzufügen</h2>
      <form @submit.prevent="addNewSupplier">
        <div class="mb-4">
          <label for="supplierName" class="block font-medium">Name des Lieferanten *</label>
          <input
            type="text"
            id="supplierName"
            v-model="newSupplier.name"
            required
            placeholder="Lieferantenname eingeben"
            class="border border-gray-300 rounded px-3 py-2 w-full"
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
            class="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
          >
            Abbrechen
          </button>
          <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Speichern
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import API_URL from '@/api';
import PdfViewer from './PdfViewer.vue';
import {
  showSnackbar,
  snackbarMessage,
  snackbarType,
  showSnackbarMessage,
} from '@/composables/useSnackbar';

// Formular-Referenzen
const uploadForm = ref(null); // Referenz auf das Upload-Formular
// const selectedFile = ref(null); // Speichert die ausgewählte Datei

// Reaktive Zustände für die Belegarten und Dokumentdaten
const categoryType = ref(); // Belegart (Radio-Button Markierung)
const positions = ref([{ betrag: '', description: '', categoryName: '', umsatzsteuer: '' }]); // Positionen (Buchungsdaten)

// Reaktive Zustände für Umsatzsteuer
const taxRates = ref([]); // Optionen für das Umsatzsteuer-Dropdown
const newTaxRate = ref({ name: '', percentage: '', valid_from: '' }); // Neue Umsatzsteuer-Daten

// Modal- und Dateizustände
const showTaxRateModal = ref(false); // Zeigt das Modal für neue Umsatzsteuer an
const showSupplierModal = ref(false);
const isFileUploaded = ref(false); // Prüft, ob ein Dokument hochgeladen wurde

// Reaktive Zustände für Dokumenteninformationen
const documentDetails = ref({
  document_type: '',
  status: 'OPEN',
  number: '',
  document_date: '',
  supplier_id: '',
  delivery_date: '',
  link_id: '',
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

const suppliers = ref([]); // Optionen für das Lieferanten-Dropdown
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
    betrag: '',
    description: '',
    categoryName: '',
    umsatzsteuer: '',
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
};

const updateFileUploaded = (fileDetails) => {
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

  // Füge die Upload-Daten hinzu
  formData.append('filename', documentDetails.value.filename);
  formData.append('file_path', documentDetails.value.file_path);
  formData.append('mimetype', documentDetails.value.mimetype);
  formData.append('file_size', documentDetails.value.file_size);

  // Füge die Positionen als JSON-Array hinzu
  formData.append('positions', JSON.stringify(positions.value));

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
      showSnackbarMessage('Beleg erfolgreich hochgeladen!', 'success');

      file.value = null;
      description.value = '';
      categoryName.value = '';
      categoryType.value = '';
      belegDatum.value = '';
      betrag.value = '';
      steuerart.value = '';
      lieferdatum.value = '';
      lieferant.value = '';
      verknuepfung.value = '';
      faelligkeit.value = '';
      kostenstelle.value = '';
      tags.value = '';
      positions.value = [{ betrag: '', description: '', categoryName: '', Umsatzsteuer: '' }];
      document.getElementById('file').value = '';

      //emit('document-uploaded');
    } else {
      showSnackbarMessage('Fehler beim hochladen', 'error');
    }
  } catch (error) {
    console.error('Upload-Fehler:', error);
    showSnackbarMessage('Ein unerwarteter Fehler ist aufgetreten.', 'error');
  }
};

onMounted(() => {
  fetchTaxRates();
  fetchSuppliers();
});
</script>

<style scoped></style>
