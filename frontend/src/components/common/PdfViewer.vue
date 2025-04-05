<template>
  <div class="pdf-viewer">
    <!-- Datei-Upload Bereich -->
    <file-upload-area v-if="!fileUploaded" @file-selected="handleFileChange" />

    <!-- Bild-Anzeige -->
    <image-preview v-if="fileType === 'image'" :src="fileUrl" @delete="deleteFile" />

    <!-- PDF-Anzeige -->
    <pdf-document-viewer
      v-if="fileType === 'pdf'"
      :current-page="currentPage"
      :total-pages="totalPages"
      @delete="deleteFile"
      @prev-page="prevPage"
      @next-page="nextPage"
    >
      <canvas ref="pdfCanvas" class="w-full"></canvas>
    </pdf-document-viewer>
  </div>
</template>

<script setup>
import { ref, defineAsyncComponent } from 'vue';
import * as pdfjsLib from 'pdfjs-dist';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import { XMarkIcon } from '@heroicons/vue/24/solid';

// Komponenten für bessere Lesbarkeit und Wartbarkeit
const FileUploadArea = defineAsyncComponent(() =>
  import('./PdfViewerComponents/FileUploadArea.vue')
);
const ImagePreview = defineAsyncComponent(() => import('./PdfViewerComponents/ImagePreview.vue'));
const PdfDocumentViewer = defineAsyncComponent(() =>
  import('./PdfViewerComponents/PdfDocumentViewer.vue')
);

// PDF.js Worker initialisieren
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

// Emits definieren
const emit = defineEmits(['file-selected', 'file-deleted']);

// Zustandsvariablen
const fileUrl = ref(null);
const fileType = ref(null);
const pdfCanvas = ref(null);
const currentPage = ref(1);
const totalPages = ref(0);
const fileUploaded = ref(false);
let pdfDocument = null;

/**
 * Rendert eine PDF-Seite im Canvas
 */
const renderPage = async (pageNumber) => {
  if (!pdfDocument) return;

  const page = await pdfDocument.getPage(pageNumber);

  // Höhere Qualität für bessere Lesbarkeit
  const highQualityScale = 3;
  const viewport = page.getViewport({ scale: highQualityScale });

  const canvas = pdfCanvas.value;
  if (!canvas) return;

  const context = canvas.getContext('2d');
  canvas.width = viewport.width;
  canvas.height = viewport.height;

  await page.render({ canvasContext: context, viewport }).promise;
};

/**
 * Verarbeitet die Dateiauswahl
 */
const handleFileChange = async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;

  fileUploaded.value = true;
  const fileMime = file.type;

  try {
    if (fileMime.startsWith('image/')) {
      // Bildverarbeitung
      fileType.value = 'image';
      fileUrl.value = URL.createObjectURL(file);
      emit('file-selected', file);
    } else if (fileMime === 'application/pdf') {
      // PDF-Verarbeitung
      fileType.value = 'pdf';
      const arrayBuffer = await file.arrayBuffer();
      pdfDocument = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
      totalPages.value = pdfDocument.numPages;
      currentPage.value = 1;
      await renderPage(currentPage.value);
      emit('file-selected', file);
    } else {
      // Nicht unterstütztes Format
      fileType.value = null;
      fileUrl.value = null;
      alert('Nur PDF, PNG oder JPG werden unterstützt.');
    }
  } catch (error) {
    console.error('Fehler beim Verarbeiten der Datei:', error);
    alert('Fehler beim Verarbeiten der Datei. Bitte versuchen Sie es erneut.');
    deleteFile();
  }
};

/**
 * Navigation: Nächste PDF-Seite
 */
const nextPage = async () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    await renderPage(currentPage.value);
  }
};

/**
 * Navigation: Vorherige PDF-Seite
 */
const prevPage = async () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    await renderPage(currentPage.value);
  }
};

/**
 * Löscht die aktuell angezeigte Datei
 */
const deleteFile = () => {
  if (fileUrl.value) {
    URL.revokeObjectURL(fileUrl.value);
  }

  // Zustand zurücksetzen
  fileUrl.value = null;
  fileType.value = null;
  fileUploaded.value = false;
  pdfDocument = null;
  currentPage.value = 1;
  totalPages.value = 0;

  emit('file-deleted', null);
};

// Methoden für externe Komponenten verfügbar machen
defineExpose({
  deleteFile,
});
</script>

<style scoped>
.pdf-viewer {
  width: 100%;
  height: 100%;
}

canvas {
  display: block;
  max-width: 100%;
}
</style>
