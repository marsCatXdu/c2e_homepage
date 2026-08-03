import professors from '../data/professors.json';

export type Professor = (typeof professors)[number];

/** Longer aliases first so "Danny H.K. Tsang" matches before "Danny Tsang". */
function aliasPattern(aliases: string[]): RegExp {
  const escaped = [...aliases]
    .sort((a, b) => b.length - a.length)
    .map((a) => a.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  return new RegExp(`(${escaped.join('|')})`, 'g');
}

export function displayProfessorName(prof: Professor, locale: 'en' | 'zh-cn', form: 'full' | 'short' = 'full'): string {
  const en = form === 'short' && 'short' in prof && prof.short ? prof.short : prof.en;
  return locale === 'zh-cn' ? `${en}（${prof.zh}）` : en;
}

export type TextPart =
  | { type: 'text'; value: string }
  | { type: 'prof'; value: string; href: string };

function isShortMatch(raw: string, prof: Professor): boolean {
  const short = 'short' in prof ? (prof as { short?: string }).short : undefined;
  if (!short) return false;
  return (
    raw === short ||
    raw === `Prof. ${short}` ||
    raw === `Professor ${short}` ||
    raw.endsWith(short) && !/H\.?\s*K\.?/i.test(raw) && !/Hin Kwok/i.test(raw)
  );
}

/** Split text into plain segments and linked professor name segments. */
export function linkifyProfessorParts(text: string, locale: 'en' | 'zh-cn' = 'en'): TextPart[] {
  const catalog = professors.map((p) => ({
    ...p,
    pattern: aliasPattern([...p.aliases, p.en, p.zh, displayProfessorName(p, 'zh-cn')]),
  }));

  // Build a global matcher from all aliases
  const allAliases = catalog.flatMap((p) => {
    const short = 'short' in p ? (p as { short?: string }).short : undefined;
    return [
      ...p.aliases,
      p.en,
      p.zh,
      displayProfessorName(p, 'zh-cn'),
      ...(short ? [short, displayProfessorName(p, 'zh-cn', 'short')] : []),
    ];
  });
  const unique = [...new Set(allAliases)].sort((a, b) => b.length - a.length);
  const global = new RegExp(
    `(${unique.map((a) => a.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})`,
    'g',
  );

  const parts: TextPart[] = [];
  let last = 0;
  for (const match of text.matchAll(global)) {
    const start = match.index ?? 0;
    const raw = match[0];
    if (start > last) {
      parts.push({ type: 'text', value: text.slice(last, start) });
    }
    const prof = catalog.find(
      (p) =>
        p.en === raw ||
        p.zh === raw ||
        p.aliases.includes(raw) ||
        displayProfessorName(p, 'zh-cn') === raw ||
        displayProfessorName(p, 'zh-cn', 'short') === raw ||
        (('short' in p && (p as { short?: string }).short === raw)),
    );
    if (prof) {
      const form = isShortMatch(raw, prof) ? 'short' : 'full';
      parts.push({
        type: 'prof',
        value: displayProfessorName(prof, locale, form),
        href: prof.url,
      });
    } else {
      parts.push({ type: 'text', value: raw });
    }
    last = start + raw.length;
  }
  if (last < text.length) {
    parts.push({ type: 'text', value: text.slice(last) });
  }
  return parts.length ? parts : [{ type: 'text', value: text }];
}

export function getProfessor(id: string): Professor | undefined {
  return professors.find((p) => p.id === id);
}
