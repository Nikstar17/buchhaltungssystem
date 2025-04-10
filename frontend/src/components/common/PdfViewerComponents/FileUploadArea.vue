<template>
  <div
    class="file-upload-area flex items-center justify-center [height:calc(100svh)] border-2 border-dashed p-8"
    :class="{ 'border-primary bg-primary/10': isDragging, 'border-gray-300': !isDragging }"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleFileDrop"
  >
    <div class="text-center">
      <input
        type="file"
        ref="fileInput"
        @change="$emit('file-selected', $event)"
        accept=".pdf,image/png,image/jpeg"
        class="file-input hidden"
        id="file-input"
      />
      <label
        for="file-input"
        class="cursor-pointer block mb-2 p-4 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <div class="text-xl mb-2"><i class="fas fa-upload mr-2"></i>Dateien hochladen</div>
        <p class="text-sm text-gray-500">
          Klicken Sie, um eine Datei auszuwählen oder ziehen Sie die Datei hierher
        </p>
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { showSnackbarMessage } from '@/composables/useSnackbar';

defineEmits(['file-selected']);

const isDragging = ref(false);
const fileInput = ref(null);
const MAX_FILE_SIZE = 2 * 1024 * 1024; // 2 MB in bytes

const validateFileSize = (file) => {
  if (file.size > MAX_FILE_SIZE) {
    showSnackbarMessage('Die Datei ist zu groß. Maximale Dateigröße: 2 MB.', 'error');
    return false;
  }
  return true;
};

const handleFileDrop = (event) => {
  isDragging.value = false;
  const files = event.dataTransfer.files;
  console.log(files);
  if (files.length > 0) {
    // Prüfe die Dateigröße
    if (!validateFileSize(files[0])) {
      return;
    }

    // Erstelle ein simuliertes Event mit der abgelegten Datei
    const fileEvent = {
      target: {
        files: files,
      },
    };
    // Emittiere das Event wie bei einem normalen Datei-Input
    if (fileEvent.target.files.length > 0) {
      fileInput.value.files = files; // Setze die Datei im Input-Element
      fileEvent.target.value = ''; // Setze den Wert zurück, damit derselbe File erneut ausgewählt werden kann
      fileInput.value.dispatchEvent(new Event('change')); // Löse ein Change-Event aus
    }
  }
};
</script>

<style scoped>
.file-upload-area {
  width: 100%;
  transition: all 0.3s ease;
}

.file-input {
  cursor: pointer;
}
</style>
