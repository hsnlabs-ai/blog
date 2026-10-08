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
- **Localization and Invariants:**
  - **English Posts (`docs/post/`):**
    - Rótulo: `WANT TO DISCUSS THIS ARCHITECTURE?`
    - Título: `Ask Hugo Soares, Founder & CPTO`
    - CTA: `Get in Touch` (`mailto:hugo@hsnlabs.ai?subject=Blog Architecture Inquiry - HSN Labs`)
  - **Portuguese Posts (`docs/pt/post/`):**
    - Rótulo: `QUER DISCUTIR ESTA ARQUITETURA?`
    - Título: `Fale com Hugo Soares, Founder e CPTO`
    - CTA: `Entrar em Contato` (`mailto:hugo@hsnlabs.ai?subject=Consulta Blog - HSN Labs`)
    - **Strict Zero-Parentheses Invariant:** Zero parentheses `(` and `)` permitted in visible Portuguese text, labels, or links.
  - **Geometry & Brand:**
    - Sharp 90-degree corners on card, avatar, and button (`border-radius: 0`).
    - Authentic crumpled paper texture overlay via `mix-blend-mode: multiply` at 50% opacity.
    - Official Title: Always `Founder & CPTO` (EN) or `Founder e CPTO` (PT). Never use "Arquiteto" or "Principal Architect".

