<script setup lang="ts">
defineProps({
  redirect_to: String,
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 p-6">
    <div class="bg-white shadow-lg rounded-lg p-8 max-w-md w-full text-center">
      <h1 class="text-4xl font-bold text-red-600 mb-4">404 - Page Not Found</h1>
      <p class="text-gray-700 text-lg mb-6">
        Oops! The page you're looking for doesn't exist or has been moved.
      </p>
      <p class="text-gray-600 text-sm mb-6">
        Double-check the URL, or go back to the homepage to find what you're
        looking for.
      </p>
      <a
        :href="redirect_to"
        class="text-blue-500 hover:underline text-lg font-semibold"
      >
        Return to Homepage
      </a>
    </div>
  </div>
</template>
