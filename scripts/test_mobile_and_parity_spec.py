#!/usr/bin/env python3
import glob
import re
import yaml
import json
from pathlib import Path

BLOG_DIR = Path("/Users/hugosoares/blog_hsn_labs")
SITE_DIR = Path("/Users/hugosoares/site_hsn_labs")

def test_gate_m1_parity_count():
    en_posts = list((BLOG_DIR / "docs" / "post").glob("*.md"))
    pt_posts = list((BLOG_DIR / "docs" / "pt" / "post").glob("*.md"))
    assert len(en_posts) == len(pt_posts), f"Esperado paridade EN/PT, encontrado {len(en_posts)} EN e {len(pt_posts)} PT"
    assert len(en_posts) >= 30, f"Esperado >= 30 posts EN, encontrado {len(en_posts)}"
    print(f"PASS: Gate M1 Paridade Numerica de Posts: {len(en_posts)} EN e {len(pt_posts)} PT")

def test_gate_m2_zero_parentheses_in_pt():
    pt_posts = list((BLOG_DIR / "docs" / "pt" / "post").glob("*.md"))
    for p in pt_posts:
        content = p.read_text(encoding="utf-8")
        assert "(" not in content and ")" not in content, f"ERRO: Parenteses encontrados em {p.name}"
    print(f"PASS: Gate M2 Invariante Zero Parenteses validado em todos os {len(pt_posts)} posts PT")

def test_gate_m3_no_essays_in_pt():
    pt_posts = list((BLOG_DIR / "docs" / "pt" / "post").glob("*.md"))
    for p in pt_posts:
        content = p.read_text(encoding="utf-8").lower()
        assert "ensaio" not in content and "essays" not in content, f"ERRO: Termo ensaio encontrado em {p.name}"
    print(f"PASS: Gate M3 Extincao de Termos Ensaio validada em todos os {len(pt_posts)} posts PT")

def test_gate_m4_responsive_tables_css():
    extra_css = (BLOG_DIR / "docs" / "stylesheets" / "extra.css").read_text(encoding="utf-8")
    assert "table" in extra_css, "Regra de table nao encontrada em extra.css"
    assert "overflow-x: auto" in extra_css, "Declaracao overflow-x: auto nao encontrada para tabelas"
    print("PASS: Gate M4 Responsividade de Tabelas validada no CSS")

def test_gate_m5_sitemaps_parity():
    site_sitemap = (SITE_DIR / "sitemap.xml").read_text(encoding="utf-8")
    routes_data = json.loads((BLOG_DIR / "i18n" / "routes-map.json").read_text(encoding="utf-8"))
    
    for item in routes_data["blog_posts"]:
        slug_en = item["slug_en"]
        slug_pt = item["slug_pt"]
        assert f"https://hsnlabs.ai/blog/post/{slug_en}/" in site_sitemap, f"Faltando EN no sitemap: {slug_en}"
        assert f"https://hsnlabs.ai/blog/pt/post/{slug_pt}/" in site_sitemap, f"Faltando PT no sitemap: {slug_pt}"
    print(f"PASS: Gate M5 Paridade de Sitemaps: todos os {len(routes_data['blog_posts'])} posts constam no sitemap central")

if __name__ == "__main__":
    print("=== INICIANDO EXECUCAO DA SUITE MOBILE E PARIDADE ===")
    test_gate_m1_parity_count()
    test_gate_m2_zero_parentheses_in_pt()
    test_gate_m3_no_essays_in_pt()
    test_gate_m4_responsive_tables_css()
    test_gate_m5_sitemaps_parity()
    print("=== TODOS OS 5 GATES PASSARAM COM SUCESSO ===")
