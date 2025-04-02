<template>
  <div class="flex min-h-screen">
    <main class="flex-1 p-6">
      <div
        class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0"
      >
        <button
          @click="navigateToUpload"
          class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 flex items-center space-x-2"
        >
          <PlusIcon class="w-5 h-5" />
          <span>Beleg hochladen</span>
        </button>
        <div class="flex space-x-2">
          <input
            type="text"
            placeholder="🔍 Suche..."
            class="px-3 py-2 rounded border border-gray-300"
          />
          <input type="month" class="px-3 py-2 rounded border border-gray-300" />
        </div>
      </div>
      <!-- TODO: Tabelle fixen -->
      <div class="bg-white shadow rounded-xl overflow-hidden">
        <table v-if="documents.length > 0" class="min-w-full text-sm text-left">
          <thead class="bg-gray-100 border-b font-semibold">
            <tr>
              <th class="px-4 py-3">Datum</th>
              <th class="px-4 py-3">Name</th>
              <th class="px-4 py-3">Kategorie</th>
              <th class="px-4 py-3">Betrag</th>
              <th class="px-4 py-3">Tags</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="document in documents"
              :key="document.id"
              class="border-b hover:bg-gray-50 cursor-pointer"
              @click="navigateToUpdate(document.id)"
            >
              <td class="px-4 py-3">
                {{
                  new Date(document.beleg_datum).toLocaleDateString('de-DE', {
                    weekday: 'short',
                    day: '2-digit',
                    month: 'long',
                    year: 'numeric',
                  })
                }}
              </td>
              <td class="px-4 py-3">{{ document.beschreibung }}</td>
              <td class="px-4 py-3">{{ document.kategorie_id }}</td>
              <td class="px-4 py-3">{{ document.betrag }} €</td>
              <td class="px-4 py-3">
                <ul>
                  <li v-for="tag in document.tags" :key="tag">{{ tag }}</li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="p-6 text-center text-gray-500">
          Noch keine Belege. Lade deinen ersten Beleg hoch!
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { PlusIcon } from '@heroicons/vue/24/solid';
import API_URL from '@/api';

const router = useRouter();
const documents = ref([]);

const fetchDocuments = async () => {
  try {
    const response = await fetch(`${API_URL}/api/documents`, {
      method: 'GET',
      credentials: 'include',
    });

    if (response.ok) {
      const data = await response.json();
      documents.value = data.sort((a, b) => new Date(b.beleg_datum) - new Date(a.beleg_datum));
    } else if (response.status === 401) {
      console.error('Nicht autorisiert. Bitte melden Sie sich erneut an.');
      window.location.href = '/login';
    } else {
      console.error('Fehler beim Laden der Belege:', response.statusText);
    }
  } catch (error) {
    console.error('Fehler beim Abrufen der Belege:', error);
  }
};

const navigateToUpload = () => {
  router.push('/dashboard/documents/upload'); // Updated route
};

const navigateToUpdate = (documentId) => {
  router.push(`/documents/${documentId}`);
};

onMounted(fetchDocuments);
</script>

<style scoped></style>
