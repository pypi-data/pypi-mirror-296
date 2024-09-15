<script setup lang="ts">
import { Link, usePage } from "@inertiajs/vue3";
import { PageProps } from "@/libs/props";
import { useDjingRoute } from "@/hooks/useDjingRoute";

const page = usePage<PageProps>();

const djing_route = useDjingRoute();

const resource_classes = page.props.djing_config.resource_classes;
</script>

<template>
  <div class="h-screen flex flex-col bg-gray-100">
    <header
      class="bg-white shadow px-6 py-3 flex justify-between items-center w-full"
    >
      <h1 class="text-2xl font-semibold">Admin Dashboard</h1>
      <nav>
        <ul class="flex space-x-4">
          <li v-if="$page.props.user">
            <form method="post" :action="djing_route('signout')">
              <button type="submit" class="text-red-500">Sign Out</button>
            </form>
          </li>

          <li v-else>
            <a
              :href="djing_route('signin')"
              class="text-green-500 hover:underline"
              >Sign In</a
            >
          </li>
        </ul>
      </nav>
    </header>

    <!-- Main content area -->
    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside class="w-64 bg-gray-800 text-white flex-shrink-0 p-4">
        <h1 class="text-lg font-bold mb-4">Resources</h1>
        <nav>
          <div>
            <div
              v-for="(items, groupName) in resource_classes"
              :key="groupName"
              class="mb-6"
            >
              <h2
                class="text-xl font-semibold text-gray-200 border-b border-gray-600 pb-2 mb-2"
              >
                {{ groupName }}
              </h2>
              <ul class="list-disc pl-5">
                <!-- Loop through each item in the group -->
                <li
                  v-for="item in items"
                  :key="item.resource_key"
                  class="mb-1 hover:bg-gray-700 rounded p-1"
                >
                  <Link
                    :href="
                      djing_route('resources', { resource: item.resource_key })
                    "
                    class="text-gray-300"
                    >{{ item.resource_plural_name }}</Link
                  >
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </aside>

      <!-- Main content (Right side) -->
      <main class="flex-1 p-6 overflow-auto bg-gray-50">
        <!-- Slot for the page content -->
        <slot />
      </main>
    </div>
  </div>
</template>
