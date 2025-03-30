<template>
  <div>
    <form @submit.prevent="uploadDocument" class="space-y-4">
      <div>
        <label for="file" class="block font-medium">Datei</label>
        <input
          type="file"
          id="file"
          @change="handleFileChange"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label for="description" class="block font-medium">Beschreibung</label>
        <input
          type="text"
          id="description"
          v-model="description"
          placeholder="Beschreibung eingeben"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label for="category" class="block font-medium">Kategorie</label>
        <select id="category" v-model="category" class="border border-gray-300 rounded px-3 py-2 w-full">
          <option value="" disabled>Kategorie auswählen</option>
          <option class="text-green-700" value="einnahme">Einnahme</option>
          <option class="text-red-700" value="ausgabe">Ausgabe</option>
        </select>
      </div>
      <div>
        <label for="beleg_datum" class="block font-medium">Belegdatum</label>
        <input
          type="date"
          id="beleg_datum"
          v-model="belegDatum"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label for="betrag" class="block font-medium">Betrag</label>
        <input
          type="number"
          id="betrag"
          v-model="betrag"
          step="0.01"
          placeholder="Betrag eingeben"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label for="steuerart" class="block font-medium">Steuerart</label>
        <select id="steuerart" v-model="steuerart" class="border border-gray-300 rounded px-3 py-2 w-full">
          <option value="" disabled>Steuerart auswählen</option>
          <option value="standard">Standard</option>
          <option value="ermäßigt">Ermäßigt</option>
          <option value="steuerfrei">Steuerfrei</option>
        </select>
      </div>
      <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700">Hochladen</button>
    </form>

    <!-- Snackbar -->
    <div
      v-if="showSnackbar"
      class="fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded shadow-lg transition-opacity duration-300"
    >
      Beleg erfolgreich hochgeladen!
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import API_URL from '@/api';

const file = ref(null);
const description = ref('');
const category = ref('');
const belegDatum = ref('');
const betrag = ref('');
const steuerart = ref('');
const showSnackbar = ref(false); // State for showing the snackbar

const handleFileChange = event => {
  file.value = event.target.files[0];
};

const uploadDocument = async () => {
  if (!file.value || !description.value || !category.value || !belegDatum.value || !betrag.value || !steuerart.value) {
    alert('Bitte alle Felder ausfüllen.');
    return;
  }

  const formData = new FormData();
  formData.append('file', file.value);
  formData.append('description', description.value);
  formData.append('category', category.value);
  formData.append('beleg_datum', belegDatum.value);
  formData.append('betrag', betrag.value);
  formData.append('steuerart', steuerart.value);

  const token = localStorage.getItem('access_token');

  try {
    const response = await fetch(`${API_URL}/api/documents`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData
    });

    if (response.ok) {
      // Show the snackbar
      showSnackbar.value = true;

      // Hide the snackbar after 3 seconds
      setTimeout(() => {
        showSnackbar.value = false;
      }, 3000);

      // Clear the form
      file.value = null;
      description.value = '';
      category.value = '';
      belegDatum.value = '';
      betrag.value = '';
      steuerart.value = '';
      document.getElementById('file').value = '';
    } else if (response.status === 401) {
      alert('Ihre Sitzung ist abgelaufen. Bitte melden Sie sich erneut an.');
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    } else {
      alert('Fehler beim Hochladen des Belegs.');
    }
  } catch (error) {
    console.error('Upload-Fehler:', error);
    alert('Ein unerwarteter Fehler ist aufgetreten.');
  }
};
</script>

<style scoped>
/* Add any additional styling if needed */
</style>
