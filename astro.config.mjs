// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// Local preview uses "/". GitHub Pages / CI should set BASE_PATH=/c2e_homepage/
const rawBase = process.env.BASE_PATH ?? '/';
const base = rawBase === '/' ? '/' : `/${rawBase.replace(/^\/+|\/+$/g, '')}/`;

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
  i18n: {
    defaultLocale: 'en',
    locales: [
      'en',
      {
        path: 'zh-cn',
        codes: ['zh-CN', 'zh', 'zh-Hans'],
      },
    ],
    routing: {
      prefixDefaultLocale: false,
    },
  },
});
