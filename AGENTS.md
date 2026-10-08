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
