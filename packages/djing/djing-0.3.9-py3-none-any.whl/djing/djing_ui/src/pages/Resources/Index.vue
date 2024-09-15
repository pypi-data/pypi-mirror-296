<script setup lang="ts">
import AuthLayout from "@/layouts/AuthLayout.vue";
import { Head } from "@inertiajs/vue3";
</script>

<template>
  <Head title="Dashboard" />

  <AuthLayout>
    <div
      class="text-center h-full flex justify-center flex-col items-center p-4 bg-white rounded-lg shadow-lg"
    >
      <h1 class="text-4xl font-bold mb-4 text-gray-800">Resources</h1>

      <div class="flex space-x-4">hello</div>
    </div>
  </AuthLayout>
</template>
