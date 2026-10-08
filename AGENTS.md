---
type: agent_guidelines
title: "AGENTS - HSN Labs Blog"
date: 2026-09-13
status: active
---

# Agent Guidelines for HSN Labs Personal Hub

When working in this repository, you must adhere to the following rules:

## 1. Identity & Tone
- **Voice:** "Caveman" style. Direct, dry, no fluff. Short sentences. State facts, then stop.
- **Perspective:** First-person ("I"). Hugo S. Nascimento is speaking. 
- **Inspiration:** Jason Liu (jxnl.co). Elite engineer who understands business mechanics and capital allocation.
- **Avoid:** Adjectives like "innovative", "cutting-edge". No corporate jargon. No hedging.

## 2. Technical Positioning
- **Focus:** Enterprise Agent Architecture. Business ontologies. ADLC.
- **Anti-Focus:** We do NOT sell chatbots. We do NOT deploy probabilistic LLMs directly into legacy IT. We do NOT sell SaaS (we sell Forward Deployed Engineering).

## 3. Target Audience
- **Level 3 Buyers:** CFOs, CEOs, Economic Buyers.
- **Metric of Success:** ROI, EBITDA, headcount replacement, BPO contract cancellation, margin expansion.

## 4. Workflows
- **Content Creation:** All new content goes into `docs/writing/`. Follow the "Executive Impact first, Technical Proof second" structure.
- **Build Tool:** Use `uv run mkdocs build` or `mkdocs serve`. Do not write raw HTML/CSS unless absolutely necessary. Rely on MkDocs Material native features.

## 5. Header Architecture & Mobile Invariants
- **Actions Order:** `Search` > `RSS` > `Github logo hsnlabs` > `EN · PT` (editorial interpunct `.lang-switch`) > `Apply for Bootcamp` (or `Inscrever no Bootcamp` in PT).
- **Navigation Menu:** Contains only editorial items (`All Posts`, `Bootcamp`, `Advisory`, `About Hugo`). No standalone language links in the nav menu.
- **Mobile Responsive Invariants (<= 640px):**
  - Navigation menu (`.blog-header-menu`) is hidden (`display: none !important;`).
  - Desktop-only elements (`.blog-header-cta` and `.header-github-link`) are hidden.
  - Search, RSS, and `.lang-switch` stay visible in `.blog-header-actions` with `gap: 8px` and 36px icon size, fitting cleanly within 360px without horizontal overflow.

## 6. Founder Callout Standard (Automatic Inheritance for All Posts)
- **Centralized Template Architecture:**
  - The Founder Callout component (`.founder-callout-card`) is embedded inside `overrides/modules/content.html`, positioned right after `{{ page.content }}` and above the navigation buttons.
  - The Sidebar Technical Leadership widget is embedded inside `overrides/modules/blog_sidebar.html`.
  - **Rule for New Posts:** Authors and agents do NOT manually paste HTML cards into post markdown files. Any new post added under `docs/post/*.md` (EN) or `docs/pt/post/*.md` (PT) automatically inherits the Founder Callout upon `uv run mkdocs build`.
- **Synchronized 5-State Rotation Engine (`assets/js/founder-rotation.js`):**
  - Rotates every 10 seconds with a smooth 0.35s crossfade between 5 curated pairs of Photo and Title Question.
  - **The 5 Linked States:**
    1. Foto 1 (`hugo_01.jpg` — Ao vivo microfone): `Have a project in mind?` (PT: `Tem um projeto em mente?`)
    2. Foto 6 (`hugo_06.jpg` — Mesa de madeira sorriso): `Let's talk about your project` (PT: `Vamos falar sobre o seu projeto?`)
    3. Foto 9 (`hugo_09.jpg` — Corredor e laptop): `Building something new?` (PT: `Pensando em construir algo novo?`)
    4. Foto 8 (`hugo_08.jpg` — Banco azul sorriso): `Want to run an idea by me?` (PT: `Quer trocar uma ideia sobre seu projeto?`)
    5. Foto 5 (`hugo_05.jpg` — Estúdio plantas executivo): `Need help getting started?` (PT: `Precisa de ajuda para comecar?`)
  - **Standardized CTA Elements (100% Identical Across all 5 States):**
    - Subtitle: `Share it with Hugo, CPTO` (EN) / `Compartilhe com Hugo, CPTO` (PT).
    - Button: `Start a Conversation` (EN) / `Iniciar Conversa` (PT).
    - Anti-Wrap Invariant: The button enforces `white-space: nowrap !important; flex-shrink: 0 !important;` to prevent two-line breaks under all screen sizes.
    - Destination: Directly targets the homepage contact section (`https://hsnlabs.ai/#contact` in EN, `https://hsnlabs.ai/pt/#contact` in PT).
- **Localization and Invariants:**
  - **Strict Zero-Parentheses Invariant:** Zero parentheses `(` and `)` permitted in visible Portuguese text, labels, or links.
  - **Geometry & Brand:** Sharp 90-degree corners on card, avatar, and button (`border-radius: 0`). Crumpled paper texture overlay via `mix-blend-mode: multiply` at 50% opacity.
  - **Official Title:** Always `Founder & CPTO` / `CPTO` (EN) or `Founder e CPTO` / `CPTO` (PT). Never use "Arquiteto" or "Principal Architect".

