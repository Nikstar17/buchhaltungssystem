<template>
  <div>
    <form @submit.prevent="updateDocument" class="space-y-4">
      <div>
        <label for="description" class="block font-medium">Beschreibung</label>
        <input
          type="text"
          id="description"
          v-model="formData.beschreibung"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label class="block font-medium">Kategorie</label>
        <div class="flex space-x-2">
          <button
            type="button"
            :class="
              formData.kategorie_id === 'ausgabe'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700'
            "
            class="px-4 py-2 rounded"
            @click="formData.kategorie_id = 'ausgabe'"
          >
            Ausgabe
          </button>
          <button
            type="button"
            :class="
              formData.kategorie_id === 'einnahme'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700'
            "
            class="px-4 py-2 rounded"
            @click="formData.kategorie_id = 'einnahme'"
          >
            Einnahme
          </button>
        </div>
      </div>
      <div>
        <label for="beleg_datum" class="block font-medium">Belegdatum</label>
        <input
          type="date"
          id="beleg_datum"
          v-model="formData.beleg_datum"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label for="betrag" class="block font-medium">Betrag</label>
        <input
          type="number"
          id="betrag"
          v-model="formData.betrag"
          step="0.01"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label for="steuerart" class="block font-medium">Steuerart</label>
        <select
          id="steuerart"
          v-model="formData.steuerart"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        >
          <option value="" disabled>Steuerart auswählen</option>
          <option value="standard">Standard</option>
          <option value="ermäßigt">Ermäßigt</option>
          <option value="steuerfrei">Steuerfrei</option>
        </select>
      </div>
      <div>
        <label for="lieferdatum" class="block font-medium">Lieferdatum</label>
        <input
          type="date"
          id="lieferdatum"
          v-model="formData.lieferdatum"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label for="lieferant" class="block font-medium">Lieferant</label>
        <input
          type="text"
          id="lieferant"
          v-model="formData.lieferant"
          placeholder="Lieferant eingeben"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label for="kostenstelle" class="block font-medium">Kostenstelle</label>
        <input
          type="text"
          id="kostenstelle"
          v-model="formData.kostenstelle"
          placeholder="Kostenstelle eingeben"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
      <div>
        <label for="tags" class="block font-medium">Tags</label>
        <input
          type="text"
          id="tags"
          v-model="formData.tags"
          placeholder="Tags eingeben (kommagetrennt)"
          class="border border-gray-300 rounded px-3 py-2 w-full"
        />
      </div>
    </form>

    <div class="flex justify-between mt-4">
      <button
        type="submit"
        class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700"
        @click="updateDocument"
      >
        Aktualisieren
      </button>
      <button
        @click="showDeleteModal = true"
        class="bg-red-600 text-white px-4 py-2 rounded shadow hover:bg-red-700"
      >
        Löschen
      </button>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded shadow-lg w-96">
        <h2 class="text-lg font-bold mb-4">Bestätigung</h2>
        <p class="mb-4">Sind Sie sicher, dass Sie dieses Dokument löschen möchten?</p>
        <div class="flex justify-end space-x-4">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
          >
            Abbrechen
          </button>
          <button
            @click="confirmDelete"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Löschen
          </button>
        </div>
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
  </div>
</template>

<script setup>
import { reactive, watch, ref } from 'vue';
import API_URL from '@/api';

const props = defineProps({
  document: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['document-updated', 'document-deleted']);

const formData = reactive({
  beschreibung: '',
  kategorie_id: '',
  beleg_datum: '',
  betrag: '',
  steuerart: '',
  lieferdatum: '',
  lieferant: '',
  kostenstelle: '',
  tags: '',
});

const showSnackbar = ref(false);
const snackbarMessage = ref('');
const snackbarType = ref('success');
const showDeleteModal = ref(false);

const displaySnackbar = (message, type = 'success') => {
  snackbarMessage.value = message;
  snackbarType.value = type;
  showSnackbar.value = true;
  setTimeout(() => {
    showSnackbar.value = false;
  }, 5000);
};

// Watch for changes in the document prop and update the form fields
watch(
  () => props.document,
  (newDocument) => {
    if (newDocument) {
      formData.beschreibung = newDocument.beschreibung || '';
      formData.kategorie_id = newDocument.kategorie_id || '';
      formData.beleg_datum = newDocument.beleg_datum
        ? new Date(newDocument.beleg_datum).toISOString().split('T')[0]
        : '';
      formData.betrag = newDocument.betrag || '';
      formData.steuerart = newDocument.steuerart || '';
      formData.lieferdatum = newDocument.lieferdatum || '';
      formData.lieferant = newDocument.lieferant || '';
      formData.kostenstelle = newDocument.kostenstelle || '';
      formData.tags = newDocument.tags || '';
    }
  },
  { immediate: true }
);

const updateDocument = async () => {
  if (
    !formData.beschreibung ||
    !formData.kategorie_id ||
    !formData.beleg_datum ||
    !formData.betrag ||
    !formData.steuerart ||
    !formData.lieferdatum ||
    !formData.lieferant ||
    !formData.kostenstelle ||
    !formData.tags
  ) {
    displaySnackbar('Bitte alle Felder ausfüllen.', 'error');
    return;
  }

  try {
    const payload = {
      ...formData,
      beleg_datum: formData.beleg_datum ? new Date(formData.beleg_datum).toISOString() : null,
    };

    let response = await fetch(`${API_URL}/api/documents/${props.document.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': csrfToken,
      },
      body: JSON.stringify(payload),
      credentials: 'include',
    });

    if (response.ok) {
      displaySnackbar('Dokument erfolgreich aktualisiert.');
      emit('document-updated');
    } else {
      displaySnackbar('Fehler beim Aktualisieren des Dokuments.', 'error');
    }
  } catch (error) {
    console.error('Fehler beim Aktualisieren:', error);
    displaySnackbar('Ein unerwarteter Fehler ist aufgetreten.', 'error');
  }
};

const confirmDelete = async () => {
  showDeleteModal.value = false;
  try {
    const csrfToken = document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrf_access_token='))
      ?.split('=')[1];

    if (!csrfToken) {
      displaySnackbar('CSRF-Token fehlt. Bitte melden Sie sich erneut an.', 'error');
      window.location.href = '/login';
      return;
    }

    const response = await fetch(`${API_URL}/api/documents/${props.document.id}`, {
      method: 'DELETE',
      headers: {
        'X-CSRF-TOKEN': csrfToken,
      },
      credentials: 'include',
    });

    if (response.ok) {
      displaySnackbar('Dokument erfolgreich gelöscht.');
      emit('document-deleted');
    } else {
      displaySnackbar('Fehler beim Löschen des Dokuments.', 'error');
    }
  } catch (error) {
    console.error('Fehler beim Löschen:', error);
    displaySnackbar('Ein unerwarteter Fehler ist aufgetreten.', 'error');
  }
};
</script>

<style scoped></style>
