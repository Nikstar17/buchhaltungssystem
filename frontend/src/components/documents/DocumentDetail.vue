<template>
  <div class="flex flex-row h-screen bg-gray-50">
    <!-- File -->
    <div class="w-2/5 overflow-y-auto p-6 rounded-lg">
      <div v-if="fileType === 'image'" class="flex items-center justify-center">
        <img :src="fileUrl" alt="Bildvorschau" class="max-w-full rounded-lg shadow-sm" />
      </div>
      <div v-if="fileType === 'pdf'" class="flex justify-center">
        <div class="canvas-container pb-5 px-5">
          <canvas ref="pdfCanvas" class="w-full rounded-lg shadow-sm"></canvas>
        </div>
      </div>
    </div>

    <!-- Details -->
    <div class="w-3/5 p-6">
      <div
        v-if="document"
        class="border border-gray-200 rounded-lg p-6 space-y-6 bg-white shadow-md"
      >
        <div class="grid grid-cols-2 gap-6">
          <div>
            <label class="block text-sm text-gray-500 font-medium mb-1">Status</label>
            <p class="text-gray-800 font-semibold">
              {{ document.status }}
            </p>
          </div>

          <div>
            <label class="block text-sm text-gray-500 font-medium mb-1">Fälligkeit</label>
            <p class="text-gray-800 font-semibold">
              {{ document.due_date ? document.due_date : '-' }}
            </p>
          </div>

          <div>
            <label class="block text-sm text-gray-500 font-medium mb-1">Belegnummer</label>
            <p class="text-gray-800 font-semibold">
              {{ document.document_number }}
            </p>
          </div>

          <div>
            <label class="block text-sm text-gray-500 font-medium mb-1">Lieferant/Kunde</label>
            <p class="text-gray-800 font-semibold">
              {{ supplierName }}
            </p>
          </div>

          <div>
            <label class="block text-sm text-gray-500 font-medium mb-1">Belegdatum</label>
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
        </div>

        <div v-if="lineItems.length" class="mt-6">
          <h2 class="text-xl font-semibold mb-4 text-gray-800">Positionen</h2>

          <table class="min-w-full bg-white border border-gray-200 rounded-lg shadow-sm">
            <thead>
              <tr class="bg-gray-100">
                <th class="px-4 py-2 text-left text-sm font-medium text-gray-600">Nr.</th>
                <th class="px-4 py-2 text-left text-sm font-medium text-gray-600">Beschreibung</th>
                <th class="px-4 py-2 text-right text-sm font-medium text-gray-600">Menge</th>
                <th class="px-4 py-2 text-right text-sm font-medium text-gray-600">Einzelpreis</th>
                <th class="px-4 py-2 text-right text-sm font-medium text-gray-600">Gesamtpreis</th>
                <th class="px-4 py-2 text-right text-sm font-medium text-gray-600">Umsatzsteuer</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="item in lineItems" :key="item.id" class="border-t hover:bg-gray-50">
                <td class="px-4 py-2 text-sm text-gray-800">
                  {{ item.line_number }}
                </td>
                <td class="px-4 py-2 text-sm text-gray-800">
                  {{ item.description }}
                </td>
                <td class="px-4 py-2 text-sm text-gray-800 text-right">
                  {{ item.quantity }}
                </td>
                <td class="px-4 py-2 text-sm text-gray-800 text-right">
                  {{ item.unit_price }}
                </td>
                <td class="px-4 py-2 text-sm text-gray-800 text-right">
                  {{ item.total_price }}
                </td>
                <td class="px-4 py-2 text-sm text-gray-800 text-right">
                  {{ getTaxRatePercentage(item.tax_rate_id) }}%
                </td>
              </tr>
            </tbody>
          </table>
          <div class="flex justify-center mt-8">
            <button
              @click="showDeleteModal = true"
              class="bg-red-400 text-white px-4 py-1 text-sm rounded shadow hover:bg-red-500 focus:outline-none focus:ring-1 focus:ring-red-300 focus:ring-offset-1 transition-transform transform hover:scale-102"
            >
              Beleg löschen
            </button>
          </div>

          <!-- Delete Confirmation Modal -->
          <div
            v-if="showDeleteModal"
            class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
          >
            <div class="bg-white rounded-lg shadow-lg p-6 w-96">
              <h2 class="text-lg font-semibold text-gray-800 mb-4">Beleg löschen</h2>
              <p class="text-gray-600 mb-6">
                Sind Sie sicher, dass Sie diesen Beleg löschen möchten? Diese Aktion kann nicht
                rückgängig gemacht werden.
              </p>
              <div class="flex justify-end space-x-4">
                <button
                  @click="showDeleteModal = false"
                  class="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
                >
                  Abbrechen
                </button>
                <button
                  @click="confirmDelete"
                  class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                  Löschen
                </button>
              </div>
            </div>
          </div>

          <div
            v-if="showSnackbar"
            :class="snackbarType === 'success' ? 'bg-green-700' : 'bg-red-700'"
            class="fixed top-4 left-1/2 transform -translate-x-1/2 text-white px-4 py-2 rounded shadow-lg transition-opacity duration-300"
          >
            {{ snackbarMessage }}
          </div>
        </div>
        <div v-else class="text-gray-500 italic mt-4">Beleg wird geladen...</div>
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
</script>

<style scoped>
/* Add subtle hover effects for table rows */
table tbody tr:hover {
  background-color: #f9fafb;
}
</style>
