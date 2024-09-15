import { computed } from "vue";
import { usePage } from "@inertiajs/vue3";

/**
 * Hook to generate URLs based on route names and parameters.
 * @returns {Function} - A function to generate URLs.
 */
export function useDjingRoute() {
  const page = usePage();

  const baseUrl = computed(() => {
    const url = page.props.djing_config.base_url;
    // Ensure base URL has proper scheme and does not end with a slash
    return url.endsWith("/") ? url.slice(0, -1) : url;
  });

  const routes = computed(() => page.props.djing_urls);

  /**
   * Generate a full URL for the given route name and parameters.
   * @param {string} routeName - The name of the route.
   * @param {Object} params - The parameters to replace in the route pattern.
   * @returns {string} - The generated URL.
   */
  function djing_route(routeName, params = {}) {
    // Get the route pattern
    const routePattern = routes.value[routeName];

    if (!routePattern) {
      throw new Error(`Route "${routeName}" not found`);
    }

    // Replace parameters in the route pattern
    let url = routePattern;

    // Find all <param> or <type:param> patterns
    url = url.replace(/<(\w+(:\w+)?)>/g, (match, paramName) => {
      const key = paramName.split(":")[1] || paramName;

      if (params[key] !== undefined) {
        return encodeURIComponent(params[key]);
      } else {
        throw new Error(`Missing parameter: ${key}`);
      }
    });

    // Build and return the full URL
    return `${baseUrl.value}/${url}`;
  }

  return djing_route;
}
