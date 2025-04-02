<template>
  <div class="p-5">
    <h1 class="text-2xl font-semibold mb-6 text-gray-800">Belegdetails</h1>

    <div v-if="document" class="border border-gray-300 rounded-lg p-5 space-y-4 bg-white shadow-sm">
      <div class="grid grid-cols-2 gap-x-6 gap-y-4">
        <div>
          <label class="block text-sm text-gray-500 font-medium mb-1">Status</label>
          <p class="text-gray-800">{{ document.status }}</p>
        </div>

        <div>
          <label class="block text-sm text-gray-500 font-medium mb-1">Fälligkeit</label>
          <p class="text-gray-800">{{ document.due_date ? document.due_date : '-' }}</p>
        </div>

        <div>
          <label class="block text-sm text-gray-500 font-medium mb-1">Belegnummer</label>
          <p class="text-gray-800">{{ document.number }}</p>
        </div>

        <div>
          <label class="block text-sm text-gray-500 font-medium mb-1">Lieferant/Kunde</label>
          <p class="text-gray-800">{{ supplierName }}</p>
        </div>

        <div>
          <label class="block text-sm text-gray-500 font-medium mb-1">Belegdatum</label>
          <p class="text-gray-800">
            {{
              new Date(document.document_date).toLocaleDateString('de-DE', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
              })
            }}
          </p>
        </div>
      </div>
    </div>

    <div v-if="lineItems.length" class="mt-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">Positionen</h2>
      <table class="min-w-full bg-white border border-gray-300 rounded-lg shadow-sm">
        <thead>
          <tr class="bg-gray-100">
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">Nr.</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500">Beschreibung</th>
            <th class="px-4 py-2 text-right text-sm font-medium text-gray-500">Menge</th>
            <th class="px-4 py-2 text-right text-sm font-medium text-gray-500">Einzelpreis</th>
            <th class="px-4 py-2 text-right text-sm font-medium text-gray-500">Gesamtpreis</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in lineItems" :key="item.id" class="border-t">
            <td class="px-4 py-2 text-sm text-gray-800">{{ item.line_number }}</td>
            <td class="px-4 py-2 text-sm text-gray-800">{{ item.description }}</td>
            <td class="px-4 py-2 text-sm text-gray-800 text-right">{{ item.quantity }}</td>
            <td class="px-4 py-2 text-sm text-gray-800 text-right">{{ item.unit_price }}</td>
            <td class="px-4 py-2 text-sm text-gray-800 text-right">{{ item.total_price }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="text-gray-500 italic mt-4">Beleg wird geladen...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import API_URL from '@/api';

const route = useRoute();
const document = ref(null);
const suppliers = ref([]); // Assuming suppliers are fetched elsewhere or passed as props
const lineItems = ref([]);

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

const supplierName = computed(() => {
  const supplier = suppliers.value.find((s) => s.id === document.value?.supplier_id);
  return supplier ? supplier.name : 'Unbekannt';
});

onMounted(() => {
  fetchSuppliers();
  fetchDocumentDetails();
  fetchLineItems();
});
</script>

<style scoped></style>
