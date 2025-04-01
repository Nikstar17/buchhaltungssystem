<template>
  <div class="py-5">
    <div v-if="!fileUploaded" class="flex items-center justify-center [height:calc(100svh-5rem)]">
      <input type="file" @change="handleFileChange" accept=".pdf,image/png,image/jpeg" />
    </div>

    <div v-if="fileType === 'image'" class="flex items-center justify-center">
      <div class="relative">
        <XMarkIcon
          @click="deleteFile"
          class="absolute top-0 right-0 bg-red-500 hover:bg-gray-500 text-white rounded-full p-2 mt-2 mr-2 h-8"
        />
        <img :src="fileUrl" alt="Bildvorschau" />
      </div>
    </div>

    <div v-if="fileType === 'pdf'">
      <div class="relative">
        <XMarkIcon
          @click="deleteFile"
          class="absolute top-16 right-0 bg-red-500 hover:bg-gray-500 text-white rounded-full p-2 mt-2 mr-2 h-8"
        />
      </div>
      <div class="flex justify-evenly mx-auto py-3">
        <button
          @click="prevPage"
          :disabled="currentPage <= 1"
          class="px-4 py-2 bg-gray-300 rounded"
        >
          Zurück
        </button>
        <span>Seite {{ currentPage }} von {{ totalPages }}</span>
        <button
          @click="nextPage"
          :disabled="currentPage >= totalPages"
          class="px-4 py-2 bg-gray-300 rounded"
        >
          Weiter
        </button>
      </div>
      <div class="canvas-container mx-auto">
        <canvas ref="pdfCanvas" class="w-full"></canvas>
      </div>
      <div class="flex justify-evenly mx-auto py-3">
        <button
          @click="prevPage"
          :disabled="currentPage <= 1"
          class="px-4 py-2 bg-gray-300 rounded"
        >
          Zurück
        </button>
        <span>Seite {{ currentPage }} von {{ totalPages }}</span>
        <button
          @click="nextPage"
          :disabled="currentPage >= totalPages"
          class="px-4 py-2 bg-gray-300 rounded"
        >
          Weiter
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import * as pdfjsLib from 'pdfjs-dist';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import { XMarkIcon } from '@heroicons/vue/24/solid';
import API_URL from '@/api';
import { showSnackbarMessage } from '@/composables/useSnackbar';

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

const emit = defineEmits(['file-selected']);
const fileUrl = ref(null);
const fileType = ref(null);
const pdfCanvas = ref(null);
const currentPage = ref(1);
const totalPages = ref(0);
const fileUploaded = ref(false);
let pdfDocument = null;

const renderPage = async (pageNumber) => {
  const page = await pdfDocument.getPage(pageNumber);

  const highQualityScale = 3; // Wert zwischen 2 und 3 ist ein guter Startpunkt
  const viewport = page.getViewport({ scale: highQualityScale });

  const canvas = pdfCanvas.value;
  const context = canvas.getContext('2d');

  canvas.width = viewport.width;
  canvas.height = viewport.height;

  await page.render({ canvasContext: context, viewport }).promise;
};

const uploadFileToServer = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const csrfToken = document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrf_access_token='))
      ?.split('=')[1];

    const response = await fetch(`${API_URL}/api/upload`, {
      method: 'POST',
      headers: {
        'X-CSRF-TOKEN': csrfToken,
      },
      body: formData,
      credentials: 'include',
    });

    if (response.ok) {
      showSnackbarMessage('Datei erfolgreich hochgeladen', 'success');
    } else {
      showSnackbarMessage('Fehler beim Hochladen der Datei.', 'error');
    }
  } catch (error) {
    showSnackbarMessage('Ein unerwarteter Fehler ist aufgetreten', 'error');
  }
};

const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  fileUploaded.value = true;

  const fileMime = file.type;

  if (fileMime.startsWith('image/')) {
    fileType.value = 'image';
    fileUrl.value = URL.createObjectURL(file);
  } else if (fileMime === 'application/pdf') {
    fileType.value = 'pdf';
    const arrayBuffer = await file.arrayBuffer();
    pdfDocument = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    totalPages.value = pdfDocument.numPages;
    currentPage.value = 1;
    await renderPage(currentPage.value);
  } else {
    fileType.value = null;
    fileUrl.value = null;
    alert('Nur PDF, PNG oder JPG werden unterstützt.');
  }

  emit('file-selected', file);
};

const nextPage = async () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    await renderPage(currentPage.value);
  }
};

const prevPage = async () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    await renderPage(currentPage.value);
  }
};

const deleteFile = () => {
  fileUrl.value = null;
  fileType.value = null;
  fileUploaded.value = false;
  pdfDocument = null;
  currentPage.value = 1;
  totalPages.value = 0;
};
</script>

<style scoped>
canvas {
  display: block;
}
</style>
