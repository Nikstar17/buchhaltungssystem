<template>
  <div class="file-upload-area flex items-center justify-center [height:calc(100svh-5rem)]">
    <input
      type="file"
      @change="$emit('file-selected', $event)"
      accept=".pdf,image/png,image/jpeg"
      class="file-input"
    />
  </div>
</template>

<script setup>
defineEmits(['file-selected']);
</script>

<style scoped>
.file-upload-area {
  width: 100%;
}

.file-input {
  cursor: pointer;
}
</style>
