<template>
  <div class="image-preview flex items-center justify-center h-screen">
    <div class="relative">
      <XMarkIcon
        @click="$emit('delete')"
        class="delete-icon absolute top-0 right-0 bg-red-500 hover:bg-gray-500 text-white rounded-full p-2 mt-2 mr-2 h-8"
      />
      <img :src="src" alt="Bildvorschau" class="preview-image" />
    </div>
  </div>
</template>

<script setup>
import { XMarkIcon } from '@heroicons/vue/24/solid';

defineProps({
  src: {
    type: String,
    required: true,
  },
});

defineEmits(['delete']);
</script>

<style scoped>
.image-preview {
  width: 100%;
}

.delete-icon {
  cursor: pointer;
  z-index: 10;
}

.preview-image {
  max-width: 100%;
  height: auto;
}
</style>
