#!/usr/bin/env python3
import json
import re
import yaml
import subprocess
from pathlib import Path
from PIL import Image

BASE_DIR = Path("/Users/hugosoares/blog_hsn_labs")
DOCS_DIR = BASE_DIR / "docs"
EN_POSTS_DIR = DOCS_DIR / "post"
PT_POSTS_DIR = DOCS_DIR / "pt" / "post"
SITE_DIR = BASE_DIR / "site"
ROUTES_FILE = BASE_DIR / "i18n" / "routes-map.json"

def test_p1_frontmatter_parity():
    with open(ROUTES_FILE, "r", encoding="utf-8") as f:
        routes_data = json.load(f)["blog_posts"]
    
    assert len(routes_data) >= 30, f"Esperado >= 30 posts no routes-map, encontrado {len(routes_data)}"
    
    for item in routes_data:
        slug_en = item["slug_en"]
        slug_pt = item["slug_pt"]
        
        en_path = EN_POSTS_DIR / f"{slug_en}.md"
        pt_path = PT_POSTS_DIR / f"{slug_pt}.md"
        
        assert en_path.exists(), f"Arquivo EN ausente: {en_path}"
        assert pt_path.exists(), f"Arquivo PT ausente: {pt_path}"
        
        en_meta = yaml.safe_load(en_path.read_text(encoding="utf-8").split("---")[1]) or {}
        pt_meta = yaml.safe_load(pt_path.read_text(encoding="utf-8").split("---")[1]) or {}
        
        en_img = en_meta.get("image")
        pt_img = pt_meta.get("image")
        
        expected_img = f"assets/images/posts/{slug_en}/cover.webp"
        assert en_img == expected_img, f"Frontmatter EN de {slug_en} com image incorreta: '{en_img}' != '{expected_img}'"
        assert pt_img == expected_img, f"Frontmatter PT de {slug_pt} com image incorreta: '{pt_img}' != '{expected_img}'"
        assert en_img == pt_img, f"Desalinhamento EN/PT de imagem em {slug_en}: {en_img} != {pt_img}"
        
    print(f"PASS: Gate P1 Frontmatter Parity Validado em 100% dos {len(routes_data)} pares de artigos")

def test_p2_physical_asset_integrity():
    with open(ROUTES_FILE, "r", encoding="utf-8") as f:
        routes_data = json.load(f)["blog_posts"]
        
    for item in routes_data:
        slug_en = item["slug_en"]
        img_rel = f"assets/images/posts/{slug_en}/cover.webp"
        img_full = DOCS_DIR / img_rel
        
        assert img_full.exists(), f"Arquivo de imagem ausente no disco: {img_full}"
        size_kb = img_full.stat().st_size / 1024
        assert size_kb <= 150, f"Imagem {img_rel} excede 150 KB ({size_kb:.1f} KB)"
        
        with Image.open(img_full) as im:
            assert im.format == "WEBP", f"Formato invalido para {img_rel}: {im.format}"
            assert im.size == (1200, 675), f"Dimensoes fora do padrao 16:9 (1200x675) em {img_rel}: {im.size}"
            
    print(f"PASS: Gate P2 Integridade Fisica dos {len(routes_data)} Ativos de Imagem (1200x675 WebP, < 150 KB)")

def test_p3_zero_parentheses_in_pt():
    pt_files = list(PT_POSTS_DIR.glob("*.md"))
    for p in pt_files:
        content = p.read_text(encoding="utf-8")
        assert "(" not in content and ")" not in content, f"ERRO: Parenteses encontrados em {p.name}"
    print(f"PASS: Gate P3 Invariante Zero Parenteses Validada em todos os {len(pt_files)} arquivos PT")

def test_p4_template_and_css_contracts():
    content_template = (BASE_DIR / "overrides" / "modules" / "content.html").read_text(encoding="utf-8")
    assert "article-hero-figure" in content_template, "Classe article-hero-figure ausente em overrides/modules/content.html"
    assert "page.meta.image" in content_template, "Variavel page.meta.image ausente no template content.html"
    
    extra_css = (DOCS_DIR / "stylesheets" / "extra.css").read_text(encoding="utf-8")
    assert ".article-hero-figure" in extra_css, "Classe .article-hero-figure ausente em extra.css"
    assert ".blog-row-thumb" in extra_css, "Classe .blog-row-thumb ausente em extra.css"
    print("PASS: Gate P4 Contrato de Templates e CSS Validado")

def test_p5_strict_build():
    res = subprocess.run(["uv", "run", "mkdocs", "build", "--strict"], cwd=BASE_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"Build estrito falhou com erro:\n{res.stderr}\n{res.stdout}"
    print("PASS: Gate P5 Build Estrito do MkDocs Concluido sem Avisos ou Erros")

def test_p6_compiled_html_hero_and_thumbs():
    with open(ROUTES_FILE, "r", encoding="utf-8") as f:
        routes_data = json.load(f)["blog_posts"]
        
    for item in routes_data:
        slug_en = item["slug_en"]
        slug_pt = item["slug_pt"]
        
        en_html_file = SITE_DIR / "post" / slug_en / "index.html"
        pt_html_file = SITE_DIR / "pt" / "post" / slug_pt / "index.html"
        
        assert en_html_file.exists(), f"HTML compilado EN ausente: {en_html_file}"
        assert pt_html_file.exists(), f"HTML compilado PT ausente: {pt_html_file}"
        
        en_html = en_html_file.read_text(encoding="utf-8")
        pt_html = pt_html_file.read_text(encoding="utf-8")
        
        assert 'class="article-hero-figure"' in en_html, f"Hero figure ausente no HTML EN de {slug_en}"
        assert 'class="article-hero-figure"' in pt_html, f"Hero figure ausente no HTML PT de {slug_pt}"
        assert f"posts/{slug_en}/cover.webp" in en_html, f"Caminho da imagem ausente no HTML EN de {slug_en}"
        assert f"posts/{slug_en}/cover.webp" in pt_html, f"Caminho da imagem ausente no HTML PT de {slug_pt}"
        
    # Check index pages
    en_index = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    pt_index = (SITE_DIR / "pt" / "index.html").read_text(encoding="utf-8")
    assert 'class="blog-row-thumb"' in en_index, "Thumbs ausentes na index EN"
    assert 'class="blog-row-thumb"' in pt_index, "Thumbs ausentes na index PT"
    
    print(f"PASS: Gate P6 Verificacao em HTML Compilado Concluida em 100% dos {len(routes_data)} artigos e indices")

if __name__ == "__main__":
    print("=== EXECUTANDO SUITE DE ESPECIFICACAO DE IMAGENS E PARIDADE BILÍNGUE ===")
    test_p1_frontmatter_parity()
    test_p2_physical_asset_integrity()
    test_p3_zero_parentheses_in_pt()
    test_p4_template_and_css_contracts()
    test_p5_strict_build()
    test_p6_compiled_html_hero_and_thumbs()
    print("=== TODOS OS 6 GATES DA ESPECIFICACAO PASSARAM COM SUCESSO ===")
