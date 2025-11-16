// @ts-check
import { defineConfig } from "astro/config";
import { fileURLToPath } from "url";

import react from "@astrojs/react";
import tailwind from "@astrojs/tailwind";

import { template } from "./src/settings";

import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
    integrations: [react(), tailwind(), sitemap()],
    site: template.website_url,
    base: template.base,
    vite: {
        resolve: {
            alias: {
                "@": fileURLToPath(new URL("./src", import.meta.url)),
            },
        },
        server: {
            watch: {
                usePolling: true,
                interval: 1000,
            },
        },
    },
});
