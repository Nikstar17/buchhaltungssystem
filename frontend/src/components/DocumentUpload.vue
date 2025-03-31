<template>
  <div class="flex space-x-4 max-h-screen p-5">
    <div class="w-3/5 overflow-y-auto">
      <PdfViewer :src="filePreview" />
    </div>

    <!-- Form Section -->
    <div class="w-2/5 overflow-y-auto">
      <form @submit.prevent="uploadDocument" class="space-y-4">
        <div>
          <label class="block font-medium">Belegart</label>
          <div class="flex space-x-2">
            <button type="button" :class="categoryType === 'ausgabe' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'" class="px-4 py-2 rounded" @click="categoryType = 'ausgabe'">
              Ausgabe
            </button>
            <button type="button" :class="categoryType === 'einnahme' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'" class="px-4 py-2 rounded" @click="categoryType = 'einnahme'">
              Einnahme
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="belegnummer" class="block font-medium">Belegnummer *</label>
            <input
              type="text"
              id="belegnummer"
              v-model="belegnummer"
              required
              placeholder="Belegnummer eingeben"
              class="border border-gray-300 rounded px-3 py-2 w-full focus:invalid:border-red-500"
            />
          </div>
          <div>
            <label for="beleg_datum" class="block font-medium">Belegdatum</label>
            <input type="date" id="beleg_datum" v-model="belegDatum" class="border border-gray-300 rounded px-3 py-2 w-full" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="lieferant" class="block font-medium">Lieferant</label>
            <input type="text" id="lieferant" v-model="lieferant" placeholder="Lieferant eingeben" class="border border-gray-300 rounded px-3 py-2 w-full" />
          </div>
          <div>
            <label for="lieferdatum" class="block font-medium">Lieferdatum</label>
            <input type="date" id="lieferdatum" v-model="lieferdatum" class="border border-gray-300 rounded px-3 py-2 w-full" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="verknuepfung" class="block font-medium">Verknüpfung</label>
            <input type="text" id="verknuepfung" v-model="verknuepfung" placeholder="Verknüpfung eingeben" class="border border-gray-300 rounded px-3 py-2 w-full" />
          </div>
          <div>
            <label for="faelligkeit" class="block font-medium">Fälligkeit</label>
            <input type="date" id="faelligkeit" v-model="faelligkeit" class="border border-gray-300 rounded px-3 py-2 w-full" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="kostenstelle" class="block font-medium">Kostenstelle</label>
            <input type="text" id="kostenstelle" v-model="kostenstelle" placeholder="Kostenstelle eingeben" class="border border-gray-300 rounded px-3 py-2 w-full" />
          </div>
          <div>
            <label for="tags" class="block font-medium">Tags</label>
            <input type="text" id="tags" v-model="tags" placeholder="Tags eingeben (kommagetrennt)" class="border border-gray-300 rounded px-3 py-2 w-full" />
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
              <label :for="'betrag-' + index" class="block font-medium">Betrag</label>
              <input type="number" :id="'betrag-' + index" v-model="position.betrag" step="0.01" placeholder="Betrag eingeben" class="border border-gray-300 rounded px-3 py-2 w-full" />
            </div>
            <div>
              <label :for="'description-' + index" class="block font-medium">Beschreibung</label>
              <input type="text" :id="'description-' + index" v-model="position.description" placeholder="Beschreibung eingeben" class="border border-gray-300 rounded px-3 py-2 w-full" />
            </div>
            <div>
              <label :for="'category_name-' + index" class="block font-medium">Kategorie</label>
              <input type="text" :id="'category_name-' + index" v-model="position.categoryName" placeholder="Kategorie eingeben (z.B. Miete)" class="border border-gray-300 rounded px-3 py-2 w-full" />
            </div>
            <div>
              <label :for="'umsatzsteuer-' + index" class="block font-medium">Umsatzsteuer</label>
              <select :id="'umsatzsteuer-' + index" v-model="position.umsatzsteuer" class="border border-gray-300 rounded px-3 py-2 w-full">
                <option value="" disabled>Umsatzsteuer</option>
                <option value="standard">19%</option>
                <option value="ermäßigt">Ermäßigt</option>
                <option value="steuerfrei">Steuerfrei</option>
              </select>
            </div>
            <button v-if="index > 0" type="button" @click="removePosition(index)" class="col-span-2 bg-gray-200 text-red-700 px-4 py-2 rounded hover:bg-gray-300">Position entfernen</button>
          </div>
        </div>
        <div class="flex justify-between">
          <button type="button" @click="addPosition" class="bg-gray-200 text-gray-700 px-4 py-2 rounded shadow hover:bg-gray-300">Position hinzufügen</button>
          <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Hochladen</button>
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
</template>

<script setup>
import { ref } from 'vue';
import API_URL from '@/api';
import PdfViewer from './PdfViewer.vue'; // Import PdfViewer component

const emit = defineEmits(['document-uploaded']); // Define the event

const file = ref(null);
const filePreview = ref(null); // Define filePreview
const description = ref('');
const categoryName = ref('');
const categoryType = ref('');
const belegDatum = ref('');
const belegnummer = ref('');
const betrag = ref('');
const umsatzsteuer = ref('');
const lieferdatum = ref('');
const lieferant = ref('');
const verknuepfung = ref('');
const faelligkeit = ref('');
const kostenstelle = ref('');
const tags = ref('');
const showSnackbar = ref(false); // State for showing the snackbar
const snackbarMessage = ref('');
const snackbarType = ref('success'); // State for snackbar type (success or error)
const positions = ref([{ betrag: '', description: '', categoryName: '', umsatzsteuer: '' }]);

const handleFileChange = event => {
  const selectedFile = event.target.files[0];
  if (!selectedFile) return;

  file.value = selectedFile;
  if (file.value.type === 'application/pdf') {
    filePreview.value = URL.createObjectURL(file.value); // Generate preview URL for PDFs
  } else {
    filePreview.value = null; // Reset preview if not a PDF
  }
};

const addPosition = () => {
  positions.value.push({ betrag: '', description: '', categoryName: '', umsatzsteuer: '' });
};

const removePosition = index => {
  if (index > 0) {
    positions.value.splice(index, 1);
  }
};

const uploadDocument = async () => {
  if (
    !file.value ||
    !description.value ||
    !categoryName.value ||
    !categoryType.value ||
    !belegDatum.value ||
    !betrag.value ||
    !steuerart.value ||
    !lieferdatum.value ||
    !lieferant.value ||
    !verknuepfung.value ||
    !faelligkeit.value ||
    !kostenstelle.value ||
    !tags.value
  ) {
    snackbarMessage.value = 'Bitte alle Felder ausfüllen.';
    snackbarType.value = 'error';
    showSnackbar.value = true;
    setTimeout(() => {
      showSnackbar.value = false;
    }, 5000);
    return;
  }

  if (!positions.value.length) {
    snackbarMessage.value = 'Bitte mindestens eine Position hinzufügen.';
    snackbarType.value = 'error';
    showSnackbar.value = true;
    setTimeout(() => {
      showSnackbar.value = false;
    }, 5000);
    return;
  }

  const formData = new FormData();
  formData.append('file', file.value);
  formData.append('description', description.value);
  formData.append('category_name', categoryName.value);
  formData.append('category_type', categoryType.value);
  formData.append('beleg_datum', belegDatum.value);
  formData.append('betrag', betrag.value);
  formData.append('steuerart', steuerart.value);
  formData.append('lieferdatum', lieferdatum.value);
  formData.append('lieferant', lieferant.value);
  formData.append('verknuepfung', verknuepfung.value);
  formData.append('faelligkeit', faelligkeit.value);
  formData.append('kostenstelle', kostenstelle.value);
  formData.append('tags', tags.value);
  formData.append('positions', JSON.stringify(positions.value));

  try {
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrf_access_token='))
      ?.split('=')[1];

    const response = await fetch(`${API_URL}/api/documents`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRF-TOKEN': csrfToken
      },
      body: formData
    });

    if (response.ok) {
      snackbarMessage.value = 'Beleg erfolgreich hochgeladen!';
      snackbarType.value = 'success';
      showSnackbar.value = true;

      setTimeout(() => {
        showSnackbar.value = false;
      }, 5000);

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

      emit('document-uploaded');
    } else if (response.status === 401) {
      snackbarMessage.value = 'Ihre Sitzung ist abgelaufen. Bitte melden Sie sich erneut an.';
      snackbarType.value = 'error';
      showSnackbar.value = true;
      setTimeout(() => {
        showSnackbar.value = false;
      }, 5000);
      window.location.href = '/login';
    } else {
      snackbarMessage.value = 'Fehler beim Hochladen des Belegs.';
      snackbarType.value = 'error';
      showSnackbar.value = true;
      setTimeout(() => {
        showSnackbar.value = false;
      }, 5000);
    }
  } catch (error) {
    console.error('Upload-Fehler:', error);
    snackbarMessage.value = 'Ein unerwarteter Fehler ist aufgetreten.';
    snackbarType.value = 'error';
    showSnackbar.value = true;
    setTimeout(() => {
      showSnackbar.value = false;
    }, 5000);
  }
};
</script>

<style scoped></style>
