# HSN Labs Blog — Project Guidelines & Editorial Rules

## 1. Language Policy: 100% English Only
- All published content, engineering essays, and technical documentation must be written strictly in native, high-grade professional English.
- No Portuguese or mixed language strings are permitted in:
  - Post markdown bodies and titles
  - Post frontmatter metadata (titles, descriptions, categories, tags)
  - UI template components (CTAs, pagination, labels, navigation, search)
  - Machine-readable endpoints (llms.txt, RSS feeds, JSON feeds, schema.org JSON-LD)
  - Footer sitemaps, brand taglines, and metadata
- Target audience: Global C-Suite executives, enterprise CTOs, CIOs, and economic buyers evaluating multi-agent architectures.

## 2. Visual Identity & Design Tokens
- Primary Brand Blue: `#52B4FD` (identical to the corporate flagship site `https://hsnlabs.ai/`).
- Text Cyan / High Contrast: `#0284c7`.
- Hover Accent: `#42abfc`.
- Border Accent: `#3fa5f3`.
- Geometry: Strict 90-degree sharp corners across all buttons, containers, cards, and inputs (`border-radius: 0 !important`). Rounded corners or pill shapes are prohibited.
- Typography:
  - Editorial & Display Titles: `Cormorant Garamond`
  - Body & Interface: `Inter`
  - Code & Monospace: `Fira Code`

## 3. Layout & Structure
- Homepage (`docs/index.md`): Clean author profile with executive bio, authority proof points, and engineering essays feed. Must never display generic `HOME` page headers or automatic date stamps.
- Pagination: 10 essays per page, rendered client-side with full DOM preservation for search crawler indexing.
- Sidebar: Displays recent posts, categories, and tags with Brand Blue `#52B4FD` widget headers.

## 4. Editorial Taxonomy & Pillars
Every essay belongs to one of three canonical English pillars:
1. `Enterprise Agent Architecture`: Perimeter isolation, MCP protocols, finite state machines, legacy core integration, and runtime failure prevention.
2. `Agentic Economy & BPO Collapse`: Economic models, BPO replacement frameworks, CFO margin protection, and RPA replacement.
3. `Frontline & Case Studies`: Real-world deployments, incident audits, PoC failure root causes, and enterprise case studies (LATAM Airlines, etc.).

## 5. Machine Endpoints & SEO Infrastructure
- AI Crawler Index: `https://hsnlabs.ai/blog/llms.txt`
- RSS Feed: `https://hsnlabs.ai/blog/feed_rss_created.xml`
- JSON Feed: `https://hsnlabs.ai/blog/feed_json_created.json`
- XML Sitemap: `https://hsnlabs.ai/blog/sitemap.xml`
- Search Engine Protocol: Automated IndexNow notifications to Bing and WebSub Hub pings.
