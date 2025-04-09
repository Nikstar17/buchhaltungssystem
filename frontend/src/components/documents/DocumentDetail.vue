<template>
  <div class="flex flex-col h-screen bg-gray-50 overflow-y-auto">
    <!-- Details -->
    <div class="p-5 max-w-6xl mx-auto w-full">
      <div
        v-if="document"
        class="border border-gray-200 rounded-xl p-8 space-y-6 bg-white shadow-lg"
      >
        <div class="grid md:grid-cols-2 gap-8">
          <div>
            <label class="block text-xs uppercase tracking-wide text-gray-500 font-medium mb-1"
              >Status</label
            >
            <p class="text-gray-800 font-semibold">
              <span
                class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
              >
                {{ document.status }}
              </span>
            </p>
          </div>

          <div>
            <label class="block text-xs uppercase tracking-wide text-gray-500 font-medium mb-1"
              >Fälligkeit</label
            >
            <p class="text-gray-800 font-semibold">
              {{ document.due_date ? document.due_date : '-' }}
            </p>
          </div>

          <div>
            <label class="block text-xs uppercase tracking-wide text-gray-500 font-medium mb-1"
              >Belegnummer</label
            >
            <p class="text-gray-800 font-semibold">
              {{ document.document_number }}
            </p>
          </div>

          <div>
            <label class="block text-xs uppercase tracking-wide text-gray-500 font-medium mb-1"
              >Lieferant/Kunde</label
            >
            <p class="text-gray-800 font-semibold">
              {{ supplierName }}
            </p>
          </div>

          <div>
            <label class="block text-xs uppercase tracking-wide text-gray-500 font-medium mb-1"
              >Belegdatum</label
            >
            <p class="text-gray-800 font-semibold">
              {{
                new Date(document.issue_date).toLocaleDateString('de-DE', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                })
              }}
            </p>
          </div>
          <div>
            <label class="block text-xs uppercase tracking-wide text-gray-500 font-medium mb-1"
              >Summe</label
            >
            <p class="text-gray-800 font-semibold">
              {{ formatCurrency(lineItems.reduce((sum, item) => sum + item.total_price, 0)) }}
            </p>
          </div>

          <!-- Ensure Restbetrag is always displayed -->
          <div>
            <label class="block text-xs uppercase tracking-wide text-gray-500 font-medium mb-1"
              >Restbetrag</label
            >
            <p class="text-gray-800 font-semibold" :class="{ 'text-red-600': remainingAmount < 0 }">
              {{ formatCurrency(remainingAmount) }}
            </p>
          </div>
        </div>

        <div v-if="lineItems.length" class="mt-8">
          <h2 class="text-xl font-bold mb-4 text-gray-800 border-b pb-2">Positionen</h2>

          <div class="overflow-x-auto rounded-xl mt-4">
            <table
              class="min-w-full bg-white border border-gray-200 rounded-xl shadow-sm responsive-table"
            >
              <thead class="bg-gray-100 rounded-t-xl">
                <tr>
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
                  v-for="item in lineItems"
                  :key="item.id"
                  class="border-t hover:bg-blue-50 transition-colors duration-150"
                >
                  <td class="px-4 py-3 text-sm text-gray-800" data-label="Nr.">
                    {{ item.line_number }}
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-800" data-label="Beschreibung">
                    {{ item.description }}
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-800 text-right" data-label="Menge">
                    {{ item.quantity }}
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-800 text-right" data-label="Einzelpreis">
                    {{ formatCurrency(item.unit_price) }}
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-800 text-right" data-label="Gesamtpreis">
                    {{ formatCurrency(item.total_price) }}
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-800 text-right" data-label="Umsatzsteuer">
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
          <div class="flex justify-center mt-10">
            <button
              @click="showDeleteModal = true"
              class="bg-red-500 text-white px-5 py-2 rounded-lg shadow-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all duration-200 font-medium"
            >
              Beleg löschen
            </button>
          </div>

          <!-- Delete Confirmation Modal -->
          <div
            v-if="showDeleteModal"
            class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 animate-fade-in"
          >
            <div class="bg-white rounded-xl shadow-2xl p-8 w-full max-w-md mx-4 animate-scale-in">
              <h2 class="text-xl font-bold text-gray-800 mb-4">Beleg löschen</h2>
              <p class="text-gray-600 mb-6">
                Sind Sie sicher, dass Sie diesen Beleg löschen möchten? Diese Aktion kann nicht
                rückgängig gemacht werden.
              </p>
              <div class="flex justify-end space-x-4">
                <button
                  @click="showDeleteModal = false"
                  class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors duration-200"
                >
                  Abbrechen
                </button>
                <button
                  @click="confirmDelete"
                  class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200"
                >
                  Löschen
                </button>
              </div>
            </div>
          </div>

          <div
            v-if="showSnackbar"
            :class="snackbarType === 'success' ? 'bg-green-600/90' : 'bg-red-600/90'"
            class="fixed top-4 left-1/2 transform -translate-x-1/2 text-white px-6 py-3 rounded-xl shadow-lg transition-opacity duration-300 flex items-center"
          >
            <svg
              v-if="snackbarType === 'success'"
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
                d="M5 13l4 4L19 7"
              />
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
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            {{ snackbarMessage }}
          </div>
        </div>
        <div v-else class="text-gray-500 italic mt-4 text-center py-8">
          <svg
            class="w-12 h-12 mx-auto text-gray-300 mb-3"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16m-7 6h7"
            />
          </svg>
          Beleg wird geladen...
        </div>
      </div>
      <!-- File -->
      <div class="rounded-xl mt-6 bg-white p-2 border border-gray-200 shadow-lg">
        <div v-if="fileType === 'image'" class="flex items-center justify-center">
          <img :src="fileUrl" alt="Bildvorschau" class="max-w-full rounded-lg shadow-sm" />
        </div>
        <div v-if="fileType === 'pdf'" class="flex justify-center">
          <div class="canvas-container p-4">
            <canvas ref="pdfCanvas" class="w-full rounded-lg shadow-sm"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import API_URL from '@/api';
import * as pdfjsLib from 'pdfjs-dist';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import {
  showSnackbar,
  snackbarMessage,
  snackbarType,
  showSnackbarMessage,
} from '@/composables/useSnackbar';

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

const route = useRoute();
const router = useRouter();
const document = ref(null);
const suppliers = ref([]); // Assuming suppliers are fetched elsewhere or passed as props
const lineItems = ref([]);
const taxRates = ref([]); // Add taxRates ref

const fetchDocumentDetails = async () => {
  try {
    const response = await fetch(`${API_URL}/api/documents/${route.params.id}`, {
      method: 'GET',
      credentials: 'include',
    });

    if (response.ok) {
      document.value = await response.json();
    } else {
      console.error('Fehler beim Laden der Belegdetails:', response.statusText);
    }
  } catch (error) {
    console.error('Fehler beim Abrufen der Belegdetails:', error);
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
      console.error('Fehler beim Laden der Lieferanten:', response.statusText);
    }
  } catch (error) {
    console.error('Fehler beim Abrufen der Lieferanten:', error);
  }
};

const fetchLineItems = async () => {
  try {
    const response = await fetch(`${API_URL}/api/documents/${route.params.id}/line_items`, {
      method: 'GET',
      credentials: 'include',
    });

    if (response.ok) {
      const data = await response.json();
      lineItems.value = data.line_items;
    } else {
      console.error('Fehler beim Laden der Positionen:', response.statusText);
    }
  } catch (error) {
    console.error('Fehler beim Abrufen der Positionen:', error);
  }
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
      console.error('Fehler beim Laden der Steuersätze:', response.statusText);
    }
  } catch (error) {
    console.error('Fehler beim Abrufen der Steuersätze:', error);
  }
};

const getTaxRatePercentage = (taxRateId) => {
  const taxRate = taxRates.value.find((rate) => rate.id === taxRateId);
  return taxRate ? taxRate.percentage : 'Unbekannt';
};

const supplierName = computed(() => {
  const supplier = suppliers.value.find((s) => s.id === document.value?.supplier_id);
  return supplier ? supplier.name : 'Unbekannt';
});

const fileUrl = ref(null);
const fileType = ref(null);
const pdfCanvas = ref(null);
let pdfDocument = null;

const renderPage = async (pageNumber) => {
  const page = await pdfDocument.getPage(pageNumber);
  const viewport = page.getViewport({ scale: 2 });
  const canvas = pdfCanvas.value;
  const context = canvas.getContext('2d');
  canvas.width = viewport.width;
  canvas.height = viewport.height;
  await page.render({
    canvasContext: context,
    viewport,
  }).promise;
};

const fetchDocumentFile = async () => {
  try {
    const response = await fetch(`${API_URL}/api/uploads/base64/${route.params.id}`, {
      method: 'GET',
      credentials: 'include',
    });

    if (response.ok) {
      const data = await response.json();
      // Update to match the backend response field names
      const { mimetype, file_data } = data;

      if (mimetype.startsWith('image/')) {
        fileType.value = 'image';
        fileUrl.value = `data:${mimetype};base64,${file_data}`;
      } else if (mimetype === 'application/pdf') {
        fileType.value = 'pdf';
        const arrayBuffer = Uint8Array.from(atob(file_data), (c) => c.charCodeAt(0)).buffer;
        pdfDocument = await pdfjsLib.getDocument({
          data: arrayBuffer,
        }).promise;
        await renderPage(1);
      }
    } else {
      console.error('Fehler beim Laden der Datei:', response.statusText);
    }
  } catch (error) {
    console.error('Fehler beim Abrufen der Datei:', error);
  }
};

const deleteDocument = async () => {
  try {
    const csrfToken = window.document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrf_access_token='))
      ?.split('=')[1];

    if (!csrfToken) {
      showSnackbarMessage('CSRF-Token fehlt. Bitte melden Sie sich erneut an.', 'error');
      return;
    }

    const response = await fetch(`${API_URL}/api/documents/${document.value.id}`, {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'X-CSRF-TOKEN': csrfToken,
      },
    });

    if (response.ok) {
      router.push('/dashboard/documents');
    } else {
      const errorData = await response.json();
      console.error('Fehler beim Löschen des Belegs:', errorData.error);
      showSnackbarMessage('Fehler beim Löschen des Belegs', 'error');
    }
  } catch (error) {
    console.error('Fehler beim Löschen des Belegs:', error);
    showSnackbarMessage('Ein unerwarteter Fehler ist aufgetreten', 'error');
  }
};

const showDeleteModal = ref(false);

const confirmDelete = async () => {
  showDeleteModal.value = false;
  await deleteDocument();
};

onMounted(() => {
  fetchSuppliers();
  fetchDocumentDetails();
  fetchLineItems();
  fetchDocumentFile();
  fetchTaxRates();
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat('de-DE', {
    style: 'currency',
    currency: 'EUR',
  }).format(value);
};

// Update computed property for remaining amount
const remainingAmount = computed(() => {
  if (!document.value || !document.value.total_amount) return 0;

  const totalSelected = lineItems.value.reduce((sum, item) => sum + item.total_price, 0);
  const documentTotal = parseFloat(document.value.total_amount);

  // Allow negative values when totalSelected exceeds documentTotal
  return documentTotal - totalSelected;
});
</script>

<style scoped>
/* Add subtle hover effects for table rows */
table tbody tr:hover {
  background-color: #f0f7ff;
}

/* Responsive table styles */
@media (max-width: 767px) {
  .responsive-table {
    border: 0;
  }

  .responsive-table thead {
    display: none;
  }

  .responsive-table tr {
    display: block;
    margin-bottom: 15px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  }

  .responsive-table td {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    text-align: right;
    border-bottom: 1px solid #f3f4f6;
  }

  .responsive-table td:last-child {
    border-bottom: 0;
  }

  .responsive-table td::before {
    content: attr(data-label);
    font-weight: 600;
    text-align: left;
    color: #4b5563;
  }
}

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
