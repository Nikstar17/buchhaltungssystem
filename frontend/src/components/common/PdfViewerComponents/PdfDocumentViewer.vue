<template>
  <div class="pdf-document-viewer h-screen">
    <!-- Schließen-Button -->
    <div class="relative">
      <XMarkIcon
        @click="$emit('delete')"
        class="absolute top-24 right-5 bg-red-500 hover:bg-gray-500 text-white rounded-full p-2 mt-2 mr-2 h-8 cursor-pointer"
      />
    </div>

    <!-- Navigation -->
    <div class="flex justify-evenly mx-auto sticky top-0 z-10 bg-gray-50 py-5">
      <button
        @click="$emit('prev-page')"
        :disabled="currentPage <= 1"
        class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Zurück
      </button>

      <span class="page-info flex items-center">
        Seite {{ currentPage }} von {{ totalPages }}
      </span>

      <button
        @click="$emit('next-page')"
        :disabled="currentPage >= totalPages"
        class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Weiter
      </button>
    </div>

    <!-- Canvas-Container -->
    <div class="canvas-container">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { XMarkIcon } from '@heroicons/vue/24/solid';

defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
});

defineEmits(['delete', 'prev-page', 'next-page']);
</script>

<style scoped>
.pdf-document-viewer {
  width: 100%;
}

.page-info {
  font-weight: 500;
}

.canvas-container {
  width: 100%;
}
</style>
