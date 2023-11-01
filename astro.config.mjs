import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";

import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  output: "static",
  site: "https://www.mlplatform.org/",
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
    sitemap({
      customPages: ["https://www.mlplatform.org/tosa/tosa_spec.html"],
    }),
  ],
});
