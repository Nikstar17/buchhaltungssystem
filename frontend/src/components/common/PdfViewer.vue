<template>
  <div class="pdf-viewer h-screen">
    <!-- File upload area -->
    <file-upload-area v-if="!fileUploaded" @file-selected="handleFileChange" />

    <!-- Image display -->
    <image-preview v-if="fileType === 'image'" :src="fileUrl" @delete="deleteFile" />

    <!-- PDF display -->
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
import { showSnackbarMessage } from '@/composables/useSnackbar';

// Components for better readability and maintainability
const FileUploadArea = defineAsyncComponent(() =>
  import('./PdfViewerComponents/FileUploadArea.vue')
);
const ImagePreview = defineAsyncComponent(() => import('./PdfViewerComponents/ImagePreview.vue'));
const PdfDocumentViewer = defineAsyncComponent(() =>
  import('./PdfViewerComponents/PdfDocumentViewer.vue')
);

// Initialize PDF.js Worker
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

// Define emits
const emit = defineEmits(['file-selected', 'file-deleted']);

// State variables
const fileUrl = ref(null);
const fileType = ref(null);
const pdfCanvas = ref(null);
const currentPage = ref(1);
const totalPages = ref(0);
const fileUploaded = ref(false);
let pdfDocument = null;

/**
 * Renders a PDF page in the canvas
 */
const renderPage = async (pageNumber) => {
  if (!pdfDocument) return;

  const page = await pdfDocument.getPage(pageNumber);

  // Higher quality for better readability
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
 * Processes file selection
 */
const handleFileChange = async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;

  fileUploaded.value = true;
  const fileMime = file.type;

  try {
    if (fileMime.startsWith('image/')) {
      // Image processing
      fileType.value = 'image';
      fileUrl.value = URL.createObjectURL(file);
      emit('file-selected', file);
    } else if (fileMime === 'application/pdf') {
      // PDF processing
      fileType.value = 'pdf';
      const arrayBuffer = await file.arrayBuffer();
      pdfDocument = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
      totalPages.value = pdfDocument.numPages;
      currentPage.value = 1;
      await renderPage(currentPage.value);
      emit('file-selected', file);
    } else {
      // Unsupported format
      fileType.value = null;
      fileUrl.value = null;
      showSnackbarMessage('Nur PDF, PNG oder JPG werden unterstützt.', 'error');
    }
  } catch (error) {
    console.error('Error processing file:', error);
    showSnackbarMessage(
      'Fehler beim Verarbeiten der Datei. Bitte versuchen Sie es erneut.',
      'error'
    );
    deleteFile();
  }
};

/**
 * Navigation: Next PDF page
 */
const nextPage = async () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    await renderPage(currentPage.value);
  }
};

/**
 * Navigation: Previous PDF page
 */
const prevPage = async () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    await renderPage(currentPage.value);
  }
};

/**
 * Deletes the currently displayed file
 */
const deleteFile = () => {
  if (fileUrl.value) {
    URL.revokeObjectURL(fileUrl.value);
  }

  // Reset state
  fileUrl.value = null;
  fileType.value = null;
  fileUploaded.value = false;
  pdfDocument = null;
  currentPage.value = 1;
  totalPages.value = 0;

  emit('file-deleted', null);
};

// Make methods available for external components
defineExpose({
  deleteFile,
});
</script>

<style scoped></style>
