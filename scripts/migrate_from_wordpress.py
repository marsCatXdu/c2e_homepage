#!/usr/bin/env python3
"""Migrate content + images from the old C2E WordPress site into this Astro project."""

from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = "http://c2e.ece.ust.hk/main"
PUBLIC = ROOT / "public"
CONTENT = ROOT / "src" / "content"
DATA = ROOT / "src" / "data"

ROLE_MAP = {
    "Faculty": "faculty",
    "Research Staff": "staff",
    "Students": "student",
    "Alumni": "alumni",
}

FIELD_PAGES = {
    "smart-grids": f"{SITE}/?page_id=30",
    "cloud-edge": f"{SITE}/?page_id=28",
    "wireless": f"{SITE}/?page_id=32",
    "online-algorithms": f"{SITE}/?page_id=742",
}

NEWS_IDS = [964, 885, 646, 202, 43, 51, 47, 55, 63, 65]


def fetch(url: str, retries: int = 3) -> bytes:
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "C2E-Homepage-Migrator/1.0"},
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1 + i)
    raise RuntimeError(f"Failed to fetch {url}: {last}")


def fetch_html(url: str) -> BeautifulSoup:
    return BeautifulSoup(fetch(url), "html.parser")


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def abs_url(url: str) -> str:
    if not url:
        return url
    return urllib.parse.urljoin(SITE + "/", url)


def download(url: str, dest: Path) -> str | None:
    if not url:
        return None
    url = abs_url(url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return "/" + str(dest.relative_to(PUBLIC)).replace("\\", "/")
    try:
        data = fetch(url)
        dest.write_bytes(data)
        print(f"  image {dest.relative_to(ROOT)} ({len(data)} bytes)")
        return "/" + str(dest.relative_to(PUBLIC)).replace("\\", "/")
    except Exception as e:  # noqa: BLE001
        print(f"  WARN image failed {url}: {e}")
        return None


def yaml_escape(s: str) -> str:
    # Prefer single-quoted YAML so backslashes (e.g. math in titles) stay literal.
    s = s.replace("'", "''")
    return f"'{s}'"


def md_frontmatter(fields: dict) -> str:
    lines = ["---"]
    for k, v in fields.items():
        if v is None or v == "":
            continue
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        else:
            # Prefer quoted strings for safety
            val = str(v).replace("\n", " ").strip()
            if any(c in val for c in ':#"\'[]{}'):
                lines.append(f"{k}: {yaml_escape(val)}")
            else:
                lines.append(f"{k}: {yaml_escape(val)}")
    lines.append("---")
    return "\n".join(lines)


def clean_text(el) -> str:
    if not el:
        return ""
    text = el.get_text("\n", strip=True)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def migrate_people() -> None:
    print("Migrating people...")
    soup = fetch_html(f"{SITE}/?page_id=23")
    content = soup.select_one("#content")
    role = None
    order = {"faculty": 1, "staff": 10, "student": 100, "alumni": 1000}
    people_dir = CONTENT / "people"
    # Remove old sample people files
    for p in people_dir.glob("*.md"):
        p.unlink()

    entries = []
    for el in content.descendants:
        if getattr(el, "name", None) == "h2":
            role = ROLE_MAP.get(el.get_text(strip=True))
            continue
        if (
            getattr(el, "name", None) == "div"
            and el.get("class")
            and "cn-entry" in el.get("class")
            and role
        ):
            name_el = el.select_one(".fn")
            name = clean_text(name_el) if name_el else ""
            title_el = el.select_one(".title")
            title = clean_text(title_el) if title_el else ""
            bio_el = el.select_one(".cn-biography")
            bio = clean_text(bio_el)
            email = None
            a = el.select_one('a[href^="mailto:"]')
            if a:
                email = a.get("href", "").replace("mailto:", "").strip()
            website = None
            for link in el.select("a"):
                href = link.get("href", "")
                label = link.get_text(strip=True).lower()
                if not href.startswith("http"):
                    continue
                if "c2e.ece.ust.hk" in href or "uploads" in href:
                    continue
                if "website" in label or "internet" in label or "ece.ust" in href or "eetsang" in href:
                    website = href
                    break
            img = el.select_one("img.cn-image, img")
            photo = None
            if img and img.get("srcset"):
                photo = img["srcset"].split()[0]
            elif img and img.get("src"):
                photo = img["src"]

            slug = slugify(name.replace("Prof.", "").replace("Dr.", "").replace("Ms.", "").replace("Mr.", ""))
            local_photo = None
            if photo:
                ext = Path(urllib.parse.urlparse(photo).path).suffix or ".jpg"
                local_photo = download(photo, PUBLIC / "images" / "people" / f"{slug}{ext}")

            entries.append(
                {
                    "slug": slug,
                    "role": role,
                    "name": name,
                    "title": title,
                    "email": email,
                    "website": website,
                    "photo": local_photo,
                    "bio": bio,
                    "order": order[role],
                }
            )
            order[role] += 1

    # Alumni plain list (often one <p> with <br>-separated rows and nested links)
    alum_h2 = None
    for h in content.find_all("h2"):
        if h.get_text(strip=True) == "Alumni":
            alum_h2 = h
            break
    alumni_rows: list[dict] = []
    if alum_h2:
        for sib in alum_h2.find_all_next("p"):
            raw = str(sib)
            txt = sib.get_text(" ", strip=True)
            if "before 2013" in txt:
                alumni_note = (
                    "We have another 4 Ph.D. graduates, 32 M.Phil. graduates and "
                    "4 Postdoc alumni before 2013. See "
                    "https://eetsang.home.ece.ust.hk/thesis.html for details."
                )
                (DATA / "alumni-note.txt").write_text(alumni_note + "\n", encoding="utf-8")
                continue
            if "last modified" in txt.lower() or "Email suggestions" in txt:
                break
            if "cn-" in raw:
                continue
            if not re.search(r"(Dr\.|Mr\.|Ms\.)", txt):
                continue
            parts = re.split(r"<br\s*/?>", raw, flags=re.I)
            for part in parts:
                frag = BeautifulSoup(part, "html.parser")
                line = re.sub(r"\s+", " ", frag.get_text(" ", strip=True)).strip()
                if not re.match(r"^(Dr\.|Mr\.|Ms\.)", line):
                    continue
                website = None
                for a in frag.select("a[href]"):
                    href = a.get("href", "")
                    if href.startswith("http") and "mailto:" not in href:
                        website = href
                        break
                m = re.match(r"^(Dr\.|Mr\.|Ms\.)\s*([^(]+?)\s*(?:\((.*)\))?\s*$", line)
                if not m:
                    name, title = line, "Alumni"
                else:
                    name = f"{m.group(1)} {m.group(2).strip()}"
                    title = (m.group(3) or "Alumni").strip()
                alumni_rows.append(
                    {
                        "name": name.strip(),
                        "title": title,
                        "website": website,
                        "bio": line,
                    }
                )
            if alumni_rows:
                break

    for i, row in enumerate(alumni_rows):
        slug = slugify(row["name"])
        entries.append(
            {
                "slug": f"alumni-{slug}",
                "role": "alumni",
                "name": row["name"],
                "title": row["title"],
                "email": None,
                "website": row["website"],
                "photo": None,
                "bio": row["bio"],
                "order": 1000 + i,
            }
        )

    for e in entries:
        fm = {
            "name": e["name"],
            "role": e["role"],
            "title": e["title"] or e["role"].title(),
            "email": e["email"],
            "website": e["website"],
            "photo": e["photo"],
            "order": e["order"],
        }
        body = e["bio"] or ""
        path = people_dir / f"{e['slug']}.md"
        # ensure unique
        n = 2
        while path.exists():
            path = people_dir / f"{e['slug']}-{n}.md"
            n += 1
        path.write_text(md_frontmatter(fm) + "\n\n" + body + "\n", encoding="utf-8")
        print(f"  people/{path.name}")

    print(f"People: {len(entries)}")


def parse_pub_block(text: str, default_type: str | None = None) -> dict | None:
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("\xa0", " ")
    if not text or text.startswith("(") or text.startswith("Here is") or text.startswith(">>"):
        return None
    # [J77], [C27], or field-page style [49]
    m = re.match(r"^\[([JC])?(\d+)\]\s*(.*)$", text)
    if not m:
        return None
    kind, num, rest = m.group(1), m.group(2), m.group(3)
    qm = re.search(r"[“\"„«]\s*(.+?)\s*[”\"»]", rest)
    if not qm:
        # Some WordPress entries use two left/curly quotes
        qm = re.search(r"[“\"]\s*(.+?)\s*[“\"]", rest)
    if not qm:
        return None
    authors = rest[: qm.start()].strip().rstrip(",").strip()
    title = qm.group(1).strip()
    after = rest[qm.end() :].strip().lstrip(",").strip()
    year_m = re.search(r"(19|20)\d{2}", after)
    year = int(year_m.group(0)) if year_m else 0
    venue = after
    venue = re.sub(
        r",?\s*(accepted for publication,?|available online.*|to appear.*)$",
        "",
        venue,
        flags=re.I,
    )
    venue = re.sub(
        r",?\s*(January|February|March|April|May|June|July|August|September|October|November|December).*$",
        "",
        venue,
    )
    venue = re.sub(r",?\s*\d{4}\.?$", "", venue).strip(" ,.")
    venue = re.split(r",\s*(vol\.|Vol\.|pp\.|Issue|issue|article)", venue)[0].strip(" ,.")
    if kind == "J":
        pub_type = "journal"
        pub_id = f"j{num}"
    elif kind == "C":
        pub_type = "conference"
        pub_id = f"c{num}"
    else:
        pub_type = default_type or "journal"
        pub_id = f"field-{num}"
    return {
        "id": pub_id,
        "authors": authors,
        "title": title,
        "venue": venue,
        "year": year,
        "type": pub_type,
        "fields": [],
        "url": None,
    }


def normalize_title(t: str) -> str:
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def migrate_publications() -> None:
    print("Migrating publications...")
    pubs: dict[str, dict] = {}
    by_title: dict[str, str] = {}

    def ingest(url: str, field: str | None = None, label: str = "", default_type: str | None = None) -> None:
        print(f"  fetching {label or url}")
        soup = fetch_html(url)
        content = soup.select_one("#content .entry-content, #content")
        blocks = []
        for el in content.find_all(["p", "li"]):
            t = el.get_text(" ", strip=True).replace("\xa0", " ")
            if re.match(r"^\[([JC])?\d+\]", t):
                blocks.append(t)
        if not blocks:
            raw = content.get_text("\n", strip=True)
            parts = re.split(r"(?=\[(?:[JC])?\d+\])", raw)
            blocks = [p.strip() for p in parts if re.match(r"^\[(?:[JC])?\d+\]", p.strip())]

        for b in blocks:
            pub = parse_pub_block(b, default_type=default_type)
            if not pub:
                continue
            title_key = normalize_title(pub["title"])
            if field:
                # Match existing chronological entry by title when field pages use different numbering
                if title_key in by_title:
                    existing = pubs[by_title[title_key]]
                    if field not in existing["fields"]:
                        existing["fields"].append(field)
                    continue
                if pub["id"] in pubs:
                    if field not in pubs[pub["id"]]["fields"]:
                        pubs[pub["id"]]["fields"].append(field)
                    continue
                pub["fields"] = [field]
                # Keep field-only entries only if not already present
                pubs[pub["id"]] = pub
                by_title[title_key] = pub["id"]
            else:
                if pub["id"] in pubs:
                    continue
                pubs[pub["id"]] = pub
                by_title[title_key] = pub["id"]

    ingest(f"{SITE}/?page_id=21", label="journals", default_type="journal")
    ingest(f"{SITE}/?page_id=15", label="conferences", default_type="conference")
    for field, url in FIELD_PAGES.items():
        ingest(url, field=field, label=field)

    items = sorted(pubs.values(), key=lambda x: (-(x["year"] or 0), x["id"]))

    out = CONTENT / "publications" / "publications.yaml"
    lines = []
    for p in items:
        # Drop temporary field-only ids if they somehow remain without J/C prefix and no fields? keep all
        lines.append(f"- id: {p['id']}")
        lines.append(f"  authors: {yaml_escape(p['authors'])}")
        lines.append(f"  title: {yaml_escape(p['title'])}")
        lines.append(f"  venue: {yaml_escape(p['venue'])}")
        lines.append(f"  year: {p['year']}")
        lines.append(f"  type: {p['type']}")
        if p["fields"]:
            lines.append(f"  fields: [{', '.join(p['fields'])}]")
        else:
            lines.append("  fields: []")
        if p.get("url"):
            lines.append(f"  url: {yaml_escape(p['url'])}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    tagged = sum(1 for p in items if p["fields"])
    print(f"Publications: {len(items)} ({tagged} with field tags)")


def migrate_news() -> None:
    print("Migrating news...")
    news_dir = CONTENT / "news"
    for p in news_dir.glob("*.md"):
        p.unlink()

    # Also discover more posts from category page
    ids = list(NEWS_IDS)
    cat = fetch_html(f"{SITE}/?cat=7")
    for a in cat.select("a"):
        href = a.get("href", "")
        m = re.search(r"[?&]p=(\d+)", href)
        if m:
            ids.append(int(m.group(1)))
    ids = list(dict.fromkeys(ids))

    for pid in ids:
        url = f"{SITE}/?p={pid}"
        print(f"  post {pid}")
        try:
            soup = fetch_html(url)
        except Exception as e:  # noqa: BLE001
            print(f"  WARN skip {pid}: {e}")
            continue
        title_el = soup.select_one("h1.entry-title, .entry-title")
        title = clean_text(title_el) if title_el else f"Post {pid}"
        content = soup.select_one(".entry-content")
        if not content:
            continue
        # date
        date = None
        time_el = soup.select_one("time.entry-date, .entry-date, time")
        if time_el and time_el.get("datetime"):
            date = time_el["datetime"][:10]
        else:
            # from URL path in uploads or meta
            meta = soup.select_one('meta[property="article:published_time"]')
            if meta:
                date = meta["content"][:10]
        if not date:
            # try published text
            date = "2016-01-01"

        # featured / first image
        image = None
        img = content.select_one("img")
        if not img:
            # slider images sometimes outside
            img = soup.select_one(".entry-content img, .nivoSlider img, img.wp-post-image")
        if img:
            src = img.get("src") or (img.get("srcset") or "").split()[0]
            if src:
                ext = Path(urllib.parse.urlparse(src).path).suffix or ".jpg"
                slug = slugify(title)[:60]
                image = download(src, PUBLIC / "images" / "news" / f"{slug}{ext}")

        # body text without script
        for bad in content.select("script, style"):
            bad.decompose()
        # Convert simple paragraphs to markdown-ish
        parts = []
        for child in content.children:
            if getattr(child, "name", None) == "p":
                t = child.get_text(" ", strip=True)
                if t:
                    parts.append(t)
            elif getattr(child, "name", None) in ("ul", "ol"):
                for li in child.find_all("li"):
                    parts.append(f"- {li.get_text(' ', strip=True)}")
            elif getattr(child, "name", None) == "figure":
                continue
        body = "\n\n".join(parts).strip()
        summary = (parts[0] if parts else title)[:220]

        slug = slugify(title)[:70] or f"post-{pid}"
        fm = {
            "title": title,
            "date": date,
            "summary": summary,
            "image": image,
        }
        path = news_dir / f"{slug}.md"
        path.write_text(md_frontmatter(fm) + "\n\n" + (body or summary) + "\n", encoding="utf-8")
        print(f"  news/{path.name}")


def migrate_site_assets() -> None:
    print("Migrating site assets...")
    assets = {
        "research/smart-grids.png": "http://eez055.ee.ust.hk/main/wp-content/uploads/2019/01/smartgrid_fu.png",
        "research/cloud-edge.jpg": "http://eez055.ee.ust.hk/main/wp-content/uploads/2019/01/cloud-comput.jpg",
        "research/wireless.jpg": "http://eez055.ee.ust.hk/main/wp-content/uploads/2019/01/wireless_xxl.jpg",
        "news/group-gathering-2024.jpg": "http://c2e.ece.ust.hk/main/wp-content/uploads/2024/09/Group_Gathering_2024_Photo_for_Home_Slides.jpg",
        "news/group-gathering-2023.jpg": "http://c2e.ece.ust.hk/main/wp-content/uploads/2024/09/Group_Gathering_2023_Photo_for_Home_Slides-1.jpg",
        "hero/group-gathering-2024.jpg": "http://c2e.ece.ust.hk/main/wp-content/uploads/2024/09/Group_Gathering_2024_Photo_for_Home_Slides.jpg",
    }
    site = json.loads((DATA / "site.json").read_text(encoding="utf-8"))
    for area in site["researchAreas"]:
        key = {
            "smart-grids": "research/smart-grids.png",
            "cloud-edge": "research/cloud-edge.jpg",
            "wireless": "research/wireless.jpg",
        }.get(area["id"])
        if key and key in assets:
            local = download(assets[key], PUBLIC / "images" / key)
            area["image"] = local
    # online algorithms: reuse cloud or leave none
    for area in site["researchAreas"]:
        if area["id"] == "online-algorithms" and "image" not in area:
            area["image"] = site["researchAreas"][1].get("image")

    site["heroImage"] = download(
        assets["hero/group-gathering-2024.jpg"],
        PUBLIC / "images" / "hero" / "group-gathering-2024.jpg",
    )
    # expand about copy from old home
    soup = fetch_html(f"{SITE}/")
    # keep existing description; optionally enrich
    (DATA / "site.json").write_text(json.dumps(site, indent=2) + "\n", encoding="utf-8")
    print("  updated site.json")


def main() -> None:
    (PUBLIC / "images" / "people").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "images" / "news").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "images" / "research").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "images" / "hero").mkdir(parents=True, exist_ok=True)
    migrate_site_assets()
    migrate_people()
    migrate_news()
    migrate_publications()
    print("Done.")


if __name__ == "__main__":
    main()
