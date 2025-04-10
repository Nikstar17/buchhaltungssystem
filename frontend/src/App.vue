<script setup>
import { RouterLink, RouterView } from 'vue-router';
import {
  showSnackbar,
  showSnackbarMessage,
  snackbarMessage,
  snackbarType,
} from '@/composables/useSnackbar';
</script>

<template>
  <!-- Global Snackbar -->
  <div
    v-if="showSnackbar"
    :class="
      snackbarType === 'success'
        ? 'bg-green-600/90'
        : snackbarType === 'error'
        ? 'bg-red-600/90'
        : 'bg-blue-600/90'
    "
    class="fixed top-4 left-1/2 transform -translate-x-1/2 text-white px-6 py-3 rounded-xl shadow-lg transition-all duration-300 flex items-center z-50"
  >
    <svg
      v-if="snackbarType === 'success'"
      class="h-5 w-5 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
    </svg>
    <svg
      v-else-if="snackbarType === 'error'"
      class="h-5 w-5 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
    <svg
      v-else
      class="h-5 w-5 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
    {{ snackbarMessage }}
  </div>
  <RouterView />
</template>

<style scoped></style>
