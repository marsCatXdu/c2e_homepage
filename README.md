# C2E Group Homepage

Modern static website for the **C2E** research group (Computing, Communications, and Energy System Optimization) at HKUST.

Built with [Astro](https://astro.build) + Tailwind. Content lives in Markdown / YAML files — edit and rebuild to update.

## Quick start

Requires **Node.js 22+**.

```bash
npm install
npm run dev
```

Open the local URL shown in the terminal (usually `http://localhost:4321/c2e_homepage/`).

## Build & deploy

### GitHub Pages (default)

```bash
npm run build
```

Output: `dist/`. Pushing to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

Enable **Settings → Pages → Source: GitHub Actions** on the repository.

Default site URL: `https://marscatxdu.github.io/c2e_homepage/`

### University server (root or custom path)

Build with a root base path, then upload `dist/`:

```bash
npm run build:root
```

Or set a custom base:

```bash
BASE_PATH=/main/ npm run build
```

## Updating content

| Content | Location |
|---------|----------|
| Site name, tagline, research areas, contact | [`src/data/site.json`](src/data/site.json) |
| News posts | [`src/content/news/*.md`](src/content/news/) |
| People | [`src/content/people/*.md`](src/content/people/) |
| Publications | [`src/content/publications/publications.yaml`](src/content/publications/publications.yaml) |

### Add a news post

Create `src/content/news/my-post.md`:

```md
---
title: "Title"
date: 2026-07-28
summary: "One-line summary."
---

Body text in Markdown.
```

### Add a person

Create `src/content/people/name.md`:

```md
---
name: "Full Name"
role: student   # faculty | staff | student | alumni
title: "Ph.D. Student"
email: "you@example.com"
website: "https://example.com"   # optional
order: 20
---

Short bio.
```

### Add a publication

Append an entry to `publications.yaml`:

```yaml
- id: j78
  authors: "A. Author and D.H.K. Tsang"
  title: "Paper title"
  venue: "IEEE Transactions on ..."
  year: 2026
  type: journal   # journal | conference
  fields: [smart-grids, cloud-edge, wireless, online-algorithms]
  url: "https://doi.org/..."   # optional
```

## Pages

- `/` — Home (hero, about, research areas, recent news)
- `/news/` — News list + individual posts
- `/people/` — Team by role
- `/publications/` — Filterable sample publication list
- `/contact/` — Contact details

This is a **structure + samples** release: sample people, news, and publications only. Expand the content files over time without changing the app code.
