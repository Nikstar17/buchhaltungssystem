<template>
  <div class="p-6 bg-gray-50 text-gray-800">
    <form @submit.prevent="submitJournalEntry" class="bg-white p-6 rounded-xl shadow-sm space-y-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold text-gray-800">Neue Buchung</h2>
        <button
          type="submit"
          class="px-5 py-2.5 rounded-xl shadow-md bg-blue-600 text-white hover:bg-blue-700 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          Buchung erstellen
        </button>
      </div>

      <div class="grid grid-cols-2 gap-5">
        <div class="space-y-2">
          <label for="entry_date" class="block text-sm font-semibold text-gray-700">
            Datum *
          </label>
          <input
            type="date"
            id="entry_date"
            v-model="journalEntry.entry_date"
            required
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>

        <div class="space-y-2 relative" ref="dropdownRef">
          <label for="document_number" class="block text-sm font-semibold text-gray-700">
            Belegnummer *
          </label>
          <div class="relative">
            <input
              type="text"
              id="document_number"
              v-model="searchQuery"
              placeholder="Belegnummer suchen..."
              @focus="isDropdownOpen = true"
              @input="isDropdownOpen = true"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
            />
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
              @click="isDropdownOpen = !isDropdownOpen"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>

            <!-- Dropdown für die Suche -->
            <div
              v-if="isDropdownOpen"
              class="absolute top-full left-0 right-0 mt-1 max-h-60 overflow-y-auto bg-white z-20 border border-gray-300 rounded-lg shadow-lg"
            >
              <div
                v-if="filteredDocuments.length === 0"
                class="py-3 px-4 text-gray-500 text-center"
              >
                Keine offenen Belege gefunden
              </div>
              <div
                v-for="doc in filteredDocuments"
                :key="doc.id"
                @click="selectDocument(doc)"
                class="py-2 px-4 hover:bg-blue-50 cursor-pointer border-b border-gray-100 flex justify-between items-center"
              >
                <div>
                  <div class="font-medium text-gray-800">{{ doc.document_number }}</div>
                  <div class="text-sm text-gray-600">
                    {{ getSupplierName(doc.supplier_id) }}
                  </div>
                </div>
                <div class="text-blue-600 font-semibold">
                  {{
                    doc.calculatedTotalAmount
                      ? doc.calculatedTotalAmount.toFixed(2) + ' €'
                      : 'Kein Betrag'
                  }}
                </div>
              </div>
            </div>

            <!-- Anzeige des ausgewählten Werts -->
            <input
              type="hidden"
              name="document_number"
              v-model="journalEntry.document_number"
              required
            />
          </div>
        </div>
      </div>

      <!-- Anzeige der Document Line Items wenn ein Dokument ausgewählt ist -->
      <div
        v-if="selectedDocumentId && documentLineItems.length > 0"
        class="mt-6 bg-white rounded-lg shadow-sm border border-gray-200 p-4"
      >
        <h3 class="text-lg font-semibold text-gray-800 mb-3 border-b pb-2">Belegpositionen</h3>
        <div class="flex justify-between items-center mb-3">
          <div class="flex items-center space-x-2">
            <button
              @click="selectAllLineItems"
              class="px-3 py-1.5 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-lg text-sm font-medium transition-colors"
            >
              Alle auswählen
            </button>
            <button
              @click="deselectAllLineItems"
              class="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors"
            >
              Keinen auswählen
            </button>
          </div>
          <div class="text-right">
            <span class="text-sm text-gray-600">Ausgewählter Betrag:</span>
            <span class="ml-2 font-semibold text-gray-800">{{
              formatCurrency(selectedItemsTotal)
            }}</span>
          </div>
        </div>
        <div class="overflow-x-auto rounded-xl">
          <table class="min-w-full bg-white border border-gray-200 rounded-xl shadow-sm">
            <thead class="bg-gray-100 rounded-t-xl">
              <tr>
                <th
                  class="w-10 px-4 py-3 text-center text-xs font-semibold uppercase tracking-wider text-gray-600"
                >
                  <div class="flex justify-center">
                    <input
                      type="checkbox"
                      :checked="allItemsSelected"
                      @change="toggleAllItems"
                      class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                  </div>
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600"
                >
                  Nr.
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-600"
                >
                  Beschreibung
                </th>
                <th
                  class="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-gray-600"
                >
                  Menge
                </th>
                <th
                  class="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-gray-600"
                >
                  Einzelpreis
                </th>
                <th
                  class="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-gray-600"
                >
                  Gesamtpreis
                </th>
                <th
                  class="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-gray-600"
                >
                  Umsatzsteuer
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in documentLineItems"
                :key="item.id"
                class="border-t hover:bg-blue-50 transition-colors duration-150"
                :class="{ 'bg-blue-50': selectedLineItems.includes(item.id) }"
              >
                <td class="px-4 py-3 text-center">
                  <input
                    type="checkbox"
                    :value="item.id"
                    v-model="selectedLineItems"
                    class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </td>
                <td class="px-4 py-3 text-sm text-gray-800">{{ item.line_number }}</td>
                <td class="px-4 py-3 text-sm text-gray-800">{{ item.description }}</td>
                <td class="px-4 py-3 text-sm text-gray-800 text-right">{{ item.quantity }}</td>
                <td class="px-4 py-3 text-sm text-gray-800 text-right">
                  {{ formatCurrency(item.unit_price) }}
                </td>
                <td class="px-4 py-3 text-sm text-gray-800 text-right">
                  {{ formatCurrency(item.total_price) }}
                </td>
                <td class="px-4 py-3 text-sm text-gray-800 text-right">
                  <span
                    class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-green-100 text-green-800"
                  >
                    {{ getTaxRatePercentage(item.tax_rate_id) }}%
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Buttons für Buchungen, falls ausgewählte Positionen existieren -->
      <div
        v-if="selectedLineItems.length > 0"
        class="flex justify-between items-center mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200"
      >
        <div>
          <span class="text-sm font-medium text-gray-700"
            >{{ selectedLineItems.length }} Position(en) ausgewählt</span
          >
          <p class="text-sm text-gray-600">
            Gesamtbetrag:
            <span class="font-semibold">{{ formatCurrency(selectedItemsTotal) }}</span>
          </p>
        </div>
        <button
          @click="useSelectedItems"
          class="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Ausgewählte Positionen buchen
        </button>
      </div>

      <!-- Restbetrag anzeigen (wenn vorhanden) -->
      <div
        v-if="remainingAmount !== 0"
        class="mt-4 p-4 rounded-lg border"
        :class="remainingAmount > 0 ? 'bg-yellow-50 border-yellow-200' : 'bg-red-50 border-red-200'"
      >
        <div class="flex justify-between items-center">
          <div>
            <p class="text-sm font-medium text-gray-700">
              Restbetrag:
              <span
                class="font-semibold"
                :class="remainingAmount > 0 ? 'text-yellow-700' : 'text-red-700'"
              >
                {{ formatCurrency(remainingAmount) }}
              </span>
            </p>
          </div>
          <button
            v-if="remainingAmount > 0"
            @click="createRemainingBooking"
            class="px-5 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors focus:outline-none focus:ring-2 focus:ring-yellow-500"
          >
            Restbetrag buchen
          </button>
          <button
            v-else
            @click="createRemainingBooking"
            class="px-5 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            Differenz buchen
          </button>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-5 mt-6">
        <div class="space-y-2">
          <label for="debit_account" class="block text-sm font-semibold text-gray-700">
            Konto Soll *
          </label>
          <input
            type="text"
            id="debit_account"
            v-model="journalEntry.debit_account"
            required
            placeholder="Konto-Nr. eingeben"
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>

        <div class="space-y-2">
          <label for="credit_account" class="block text-sm font-semibold text-gray-700">
            Konto Haben *
          </label>
          <input
            type="text"
            id="credit_account"
            v-model="journalEntry.credit_account"
            required
            placeholder="Konto-Nr. eingeben"
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>
      </div>

      <div class="space-y-2">
        <label for="amount" class="block text-sm font-semibold text-gray-700"> Betrag (€) * </label>
        <input
          type="number"
          id="amount"
          v-model="journalEntry.amount"
          step="0.01"
          min="0.01"
          required
          placeholder="0,00"
          class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
        />
      </div>

      <div class="space-y-2">
        <label for="description" class="block text-sm font-semibold text-gray-700">
          Beschreibung
        </label>
        <textarea
          id="description"
          v-model="journalEntry.description"
          placeholder="Beschreibung eingeben"
          rows="3"
          class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
        ></textarea>
      </div>
    </form>
  </div>

  <!-- Snackbar für Benachrichtigungen -->
  <div
    v-if="showSnackbar"
    :class="snackbarType === 'success' ? 'bg-green-600/90' : 'bg-red-600/90'"
    class="fixed top-4 left-1/2 transform -translate-x-1/2 text-white px-6 py-3 rounded-xl shadow-lg transition-all duration-300 flex items-center"
  >
    <svg
      v-if="snackbarType === 'success'"
      class="h-5 w-5 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
    </svg>
    <svg
      v-else
      class="h-5 w-5 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
    {{ snackbarMessage }}
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount, computed } from 'vue';
import { useRouter } from 'vue-router';
import { showSnackbarMessage } from '@/composables/useSnackbar';
import DocumentService from '@/services/document.service';
import SupplierService from '@/services/supplier.service';
import TaxRateService from '@/services/tax-rate.service';
import JournalEntryService from '@/services/journal-entry.service';

const router = useRouter();

// Snackbar-Funktionalität
const showSnackbar = ref(false);
const snackbarMessage = ref('');
const snackbarType = ref('success');

// Formular-Daten
const journalEntry = ref({
  entry_date: new Date().toISOString().substr(0, 10),
  document_number: '',
  debit_account: '',
  credit_account: '',
  amount: '',
  description: '',
});

// Belegnummern-Dropdown
const openDocuments = ref([]);
const filteredDocuments = ref([]);
const searchQuery = ref('');
const isDropdownOpen = ref(false);
const suppliers = ref([]); // Für Lieferantendaten

// Referenz zum Dropdown-Container
const dropdownRef = ref(null);

// Click-outside Handler
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isDropdownOpen.value = false;
  }
};

// Holen alle offenen Belege vom Backend und berechne die Gesamtbeträge aus den Line-Items
const fetchOpenDocuments = async () => {
  try {
    // Hole Belege
    const documents = await DocumentService.getOpenDocuments();

    // Hole für jeden Beleg die zugehörigen Line-Items
    for (const doc of documents) {
      try {
        const lineItems = await DocumentService.getDocumentLineItems(doc.id);
        // Berechne den Gesamtbetrag aus den Line-Items
        doc.calculatedTotalAmount = lineItems.reduce(
          (sum, item) => sum + parseFloat(item.total_price || 0),
          0
        );
      } catch (error) {
        console.error(`Fehler beim Abrufen der Line-Items für Dokument ${doc.id}:`, error);
        doc.calculatedTotalAmount = 0;
      }
    }

    openDocuments.value = documents;
    filteredDocuments.value = documents;
  } catch (error) {
    console.error('Fehler beim Abrufen der offenen Belege:', error);
  }
};

// Lieferanten abrufen
const fetchSuppliers = async () => {
  try {
    suppliers.value = await SupplierService.getSuppliers();
  } catch (error) {
    console.error('Fehler beim Abrufen der Lieferanten:', error);
  }
};

// Lieferantennamen anhand der ID abrufen
const getSupplierName = (supplierId) => {
  const supplier = suppliers.value.find((s) => s.id === supplierId);
  return supplier ? supplier.name : 'Kein Lieferant';
};

// Filtere Belege basierend auf der Sucheingabe
const filterDocuments = () => {
  if (!searchQuery.value.trim()) {
    filteredDocuments.value = openDocuments.value;
    return;
  }

  const query = searchQuery.value.toLowerCase();
  filteredDocuments.value = openDocuments.value.filter((doc) => {
    const supplierName = getSupplierName(doc.supplier_id);
    return (
      doc.document_number.toLowerCase().includes(query) ||
      supplierName.toLowerCase().includes(query)
    );
  });
};

// State für Belegpositionen und ausgewählten Beleg
const selectedDocumentId = ref(null);
const documentLineItems = ref([]);
const taxRates = ref([]);

// Steuersätze abrufen
const fetchTaxRates = async () => {
  try {
    taxRates.value = await TaxRateService.getTaxRates();
  } catch (error) {
    console.error('Fehler beim Abrufen der Steuersätze:', error);
  }
};

// Steuersatz-Prozentsatz anhand der ID abrufen
const getTaxRatePercentage = (taxRateId) => {
  return TaxRateService.getTaxRatePercentage(taxRates.value, taxRateId);
};

// Belegpositionen für einen ausgewählten Beleg abrufen
const fetchDocumentLineItems = async (documentId) => {
  try {
    documentLineItems.value = await DocumentService.getDocumentLineItems(documentId);
  } catch (error) {
    console.error('Fehler beim Abrufen der Positionen:', error);
  }
};

// Wähle einen Beleg aus dem Dropdown aus
const selectDocument = (document) => {
  selectedDocumentId.value = document.id;
  journalEntry.value.document_number = document.document_number;
  searchQuery.value = document.document_number; // Auch das Suchfeld aktualisieren
  journalEntry.value.amount = document.calculatedTotalAmount || '';

  // Lade Belegpositionen
  fetchDocumentLineItems(document.id);

  isDropdownOpen.value = false;
};

// Currency-Formatierung
const formatCurrency = (value) => {
  return new Intl.NumberFormat('de-DE', {
    style: 'currency',
    currency: 'EUR',
  }).format(value);
};

// Überwache Änderungen der Sucheingabe
watch(searchQuery, () => {
  filterDocuments();
});

// Lade Belege beim Laden der Komponente
onMounted(() => {
  fetchSuppliers();
  fetchOpenDocuments();
  fetchTaxRates();
  document.addEventListener('click', handleClickOutside);
});

// Event-Listener beim Unmounten der Komponente entfernen
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});

const submitJournalEntry = async () => {
  try {
    await JournalEntryService.createJournalEntry(journalEntry.value);

    showSnackbarMessage('Buchung erfolgreich erstellt!', 'success');

    // Formular zurücksetzen
    journalEntry.value = {
      entry_date: new Date().toISOString().substr(0, 10),
      document_number: '',
      debit_account: '',
      credit_account: '',
      amount: '',
      description: '',
    };

    // Optional: Zur Übersichtsseite navigieren
    setTimeout(() => {
      router.push({ name: 'journal-entries' });
    }, 1500);
  } catch (error) {
    console.error('Fehler bei der Buchungserstellung:', error);
    showSnackbarMessage(error.message || 'Ein unerwarteter Fehler ist aufgetreten.', 'error');
  }
};

// State für ausgewählte Belegpositionen
const selectedLineItems = ref([]);

// Berechne den Gesamtbetrag der ausgewählten Positionen
const selectedItemsTotal = computed(() => {
  return selectedLineItems.value.reduce((sum, itemId) => {
    const item = documentLineItems.value.find((i) => i.id === itemId);
    return sum + (item ? parseFloat(item.total_price || 0) : 0);
  }, 0);
});

// Berechne den Restbetrag
const remainingAmount = computed(() => {
  return journalEntry.value.amount - selectedItemsTotal.value;
});

// Alle Positionen auswählen
const selectAllLineItems = () => {
  selectedLineItems.value = documentLineItems.value.map((item) => item.id);
};

// Alle Positionen abwählen
const deselectAllLineItems = () => {
  selectedLineItems.value = [];
};

// Toggle alle Positionen
const toggleAllItems = (event) => {
  if (event.target.checked) {
    selectAllLineItems();
  } else {
    deselectAllLineItems();
  }
};

// Prüfen, ob alle Positionen ausgewählt sind
const allItemsSelected = computed(() => {
  return selectedLineItems.value.length === documentLineItems.value.length;
});

// Ausgewählte Positionen verwenden
const useSelectedItems = () => {
  journalEntry.value.amount = selectedItemsTotal.value;

  // Generiere eine sinnvolle Beschreibung basierend auf den ausgewählten Positionen
  if (selectedLineItems.value.length === 1) {
    const item = documentLineItems.value.find((i) => i.id === selectedLineItems.value[0]);
    if (item) {
      journalEntry.value.description = item.description;
    }
  } else if (selectedLineItems.value.length > 1) {
    journalEntry.value.description = `Buchung für ${selectedLineItems.value.length} Positionen`;
  }
};

// Restbetrag separat buchen
const createRemainingBooking = () => {
  journalEntry.value.amount = Math.abs(remainingAmount.value);
  journalEntry.value.description =
    remainingAmount.value > 0 ? 'Buchung für Restbetrag' : 'Buchung für Differenzbetrag';
};
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
