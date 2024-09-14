<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 p-6">
    <div class="bg-white shadow-lg rounded-lg p-8 max-w-md w-full">
      <h1 class="text-2xl font-semibold text-red-600 mb-4">
        {{ context.error_message }}
      </h1>

      <div class="text-gray-700 text-base mb-6 space-y-2">
        <div v-for="(instruction, index) in context.instructions" :key="index">
          <div>{{ instruction }}</div>
        </div>
      </div>

      <div class="bg-gray-200 p-4 rounded-md">
        <pre class="text-sm font-mono text-gray-800">{{ context.command }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    context: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
