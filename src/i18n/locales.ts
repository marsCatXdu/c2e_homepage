export const defaultLocale = 'en' as const;
export const locales = ['en', 'zh-cn'] as const;
export type Locale = (typeof locales)[number];

export function isLocale(value: string | undefined): value is Locale {
  return locales.includes(value as Locale);
}

/** Strip site base and optional locale prefix; return path like `/news/` or `/`. */
export function stripLocaleFromPath(pathname: string, baseUrl: string): string {
  let path = pathname;
  const base = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  if (base && base !== '/' && path.startsWith(base)) {
    path = path.slice(base.length) || '/';
  }
  if (!path.startsWith('/')) path = `/${path}`;

  for (const locale of locales) {
    if (locale === defaultLocale) continue;
    if (path === `/${locale}` || path === `/${locale}/`) return '/';
    if (path.startsWith(`/${locale}/`)) {
      return path.slice(locale.length + 1) || '/';
    }
  }
  return path;
}

/** Join site base with a root-relative asset path (`/images/...`). */
export function withBase(path: string, baseUrl = import.meta.env.BASE_URL): string {
  if (!path || path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path;
  }
  const base = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;
  return `${base}${path.replace(/^\//, '')}`;
}

export function localizePath(locale: Locale, path: string, baseUrl: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`;
  const clean = normalized === '/' ? '' : normalized.replace(/\/?$/, '/');
  const base = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;

  if (locale === defaultLocale) {
    return `${base}${clean.replace(/^\//, '')}`;
  }
  return `${base}${locale}/${clean.replace(/^\//, '')}`;
}

export function getLocaleFromUrl(url: URL, baseUrl: string): Locale {
  const path = stripLocaleFromPath(url.pathname, baseUrl);
  // Prefer prefix detection from raw pathname
  const raw = url.pathname;
  const base = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  let rest = raw;
  if (base && base !== '/' && rest.startsWith(base)) {
    rest = rest.slice(base.length) || '/';
  }
  if (rest.startsWith('/zh-cn/') || rest === '/zh-cn' || rest === '/zh-cn/') {
    return 'zh-cn';
  }
  return defaultLocale;
}
