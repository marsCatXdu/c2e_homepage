// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// Local preview uses "/". GitHub Pages / CI should set BASE_PATH=/c2e_homepage
const base = process.env.BASE_PATH ?? '/';

// https://astro.build/config
export default defineConfig({
  site: 'https://marscatxdu.github.io',
  base,
  vite: {
    plugins: [tailwindcss()],
  },
  server: {
    host: '127.0.0.1',
    port: 4321,
  },
});
