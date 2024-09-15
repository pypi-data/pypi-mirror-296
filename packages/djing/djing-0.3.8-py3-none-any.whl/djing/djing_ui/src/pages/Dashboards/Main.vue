<script setup lang="ts">
import AuthLayout from "@/layouts/AuthLayout.vue";
import { Head } from "@inertiajs/vue3";
</script>

<template>
  <Head title="Dashboard" />

  <!-- Using the AuthLayout component -->
  <AuthLayout>
    <div
      class="text-center h-full flex justify-center flex-col items-center p-4 bg-white rounded-lg shadow-lg"
    >
      <h1 class="text-4xl font-bold mb-4 text-gray-800">
        Welcome, Djing Admin
      </h1>
      <p class="text-green-600 mb-5 text-lg">
        Your project is set up successfully!
      </p>
      <h3 class="text-slate-500 text-base mb-4">Powered by:</h3>

      <div class="flex space-x-4">
        <span
          class="inline-block bg-blue-500 text-white text-sm py-2 px-4 rounded-lg shadow"
        >
          Django
        </span>
        <span
          class="inline-block bg-purple-500 text-white text-sm py-2 px-4 rounded-lg shadow"
        >
          Inertia.js
        </span>
        <span
          class="inline-block bg-teal-500 text-white text-sm py-2 px-4 rounded-lg shadow"
        >
          Vue 3
        </span>
      </div>
    </div>
  </AuthLayout>
</template>
