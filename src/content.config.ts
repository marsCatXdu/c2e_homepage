import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

const news = defineCollection({
  loader: glob({ base: './src/content/news', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    summary: z.string(),
    image: z.string().optional(),
  }),
});

const people = defineCollection({
  loader: glob({ base: './src/content/people', pattern: '**/*.md' }),
  schema: z.object({
    name: z.string(),
    nameZh: z.string().optional(),
    role: z.enum(['faculty', 'staff', 'student', 'alumni']),
    title: z.string(),
    titleZh: z.string().optional(),
    email: z.string().optional(),
    website: z.string().optional(),
    photo: z.string().optional(),
    order: z.number().default(100),
    bioZh: z.string().optional(),
  }),
});

const publications = defineCollection({
  loader: file('./src/content/publications/publications.yaml'),
  schema: z.object({
    id: z.string(),
    authors: z.string(),
    title: z.string(),
    venue: z.string(),
    year: z.number(),
    type: z.enum(['journal', 'conference']),
    fields: z.array(
      z.enum([
        'smart-grids',
        'cloud-edge',
        'wireless',
        'online-algorithms',
      ]),
    ),
    url: z.string().optional(),
  }),
});

export const collections = { news, people, publications };
