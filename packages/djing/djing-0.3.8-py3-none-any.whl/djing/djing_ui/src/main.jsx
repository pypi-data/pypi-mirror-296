import Aura from "@primevue/themes/aura";
import "primeicons/primeicons.css";
import "@/index.css";

import { createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";
import "vite/modulepreload-polyfill";

import PrimeVue from "primevue/config";
import ToastService from "primevue/toastservice";

createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob("./pages/**/*.vue", { eager: true });
    return pages[`./pages/${name}.vue`];
  },
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .use(PrimeVue, {
        theme: {
          preset: Aura,
        },
      })
      .use(ToastService)
      .mount(el);
  },
});
