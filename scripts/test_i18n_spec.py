import json
import re
import sys
import glob
import yaml
from pathlib import Path

BASE_DIR = Path("/Users/hugosoares/blog_hsn_labs")
DOCS_DIR = BASE_DIR / "docs"
PT_POSTS_DIR = DOCS_DIR / "pt" / "post"
SITE_DIR = BASE_DIR / "site"
ROUTES_FILE = BASE_DIR / "i18n" / "routes-map.json"

def test_i18n_gate_1_routes_map():
    assert ROUTES_FILE.exists(), "ERRO: routes-map.json ausente"
    with open(ROUTES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    raw = json.dumps(data)
    assert "(" not in raw and ")" not in raw, "ERRO: Parenteses encontrados em routes-map.json"
    
    posts = data.get("blog_posts", [])
    assert len(posts) >= 30, f"Esperado >= 30 posts mapeados, encontrado {len(posts)}"
    
    forbidden_en_tokens = ["why", "how", "what", "graveyard", "death", "collapse", "unconstrained"]
    for p in posts:
        slug_pt = p.get("slug_pt", "")
        assert slug_pt, f"Post sem slug_pt: {p}"
        assert re.match(r"^[a-z0-9\-]+$", slug_pt), f"Slug PT com caracteres invalidos: {slug_pt}"
        for token in forbidden_en_tokens:
            assert token not in slug_pt.split("-"), f"Slug PT contem token em ingles '{token}': {slug_pt}"
            
    print(f"PASS: Gate 1 Routes Map Integro com {len(posts)} posts mapeados e slugs localizados")

def test_i18n_gate_2_pt_frontmatter_and_no_parentheses():
    posts = sorted(glob.glob(str(PT_POSTS_DIR / "*.md")))
    assert len(posts) >= 8, f"Esperado >= 8 posts traduzidos no lote piloto, encontrado {len(posts)}"
    
    for p in posts:
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
            
        assert "(" not in content and ")" not in content, f"ERRO: Parenteses encontrados em {p}"
        
        parts = content.split("---")
        assert len(parts) >= 3, f"Post {p} sem frontmatter YAML valido"
        meta = yaml.safe_load(parts[1])
        assert isinstance(meta, dict), f"Post {p} com frontmatter corrompido"
        
        title = meta.get("title")
        assert title and 10 <= len(title) <= 130, f"Post {p} titulo invalido: {title}"
        
        desc = meta.get("description")
        assert desc and 30 <= len(desc) <= 200, f"Post {p} descricao invalida: {desc}"
        
        author = meta.get("author")
        assert author == "Hugo S. Nascimento", f"Post {p} autor invalido: {author}"
        
    print(f"PASS: Gate 2 Frontmatter e Invariante Zero Parenteses Validado nos {len(posts)} posts PT")

def test_i18n_gate_3_hreflang_and_canonical():
    with open(ROUTES_FILE, "r", encoding="utf-8") as f:
        routes_data = json.load(f)
        
    posts = routes_data.get("blog_posts", [])
    tested_pairs = 0
    for p in posts:
        slug_en = p["slug_en"]
        slug_pt = p["slug_pt"]
        
        en_html = SITE_DIR / "post" / slug_en / "index.html"
        pt_html = SITE_DIR / "pt" / "post" / slug_pt / "index.html"
        
        if not en_html.exists() or not pt_html.exists():
            continue
            
        en_text = en_html.read_text(encoding="utf-8")
        pt_text = pt_html.read_text(encoding="utf-8")
        
        expected_en_url = f"https://hsnlabs.ai/blog/post/{slug_en}/"
        expected_pt_url = f"https://hsnlabs.ai/blog/pt/post/{slug_pt}/"
        
        assert f'<link rel="canonical" href="{expected_en_url}">' in en_text, f"Canonical EN incorreto em {slug_en}"
        assert f'<link rel="canonical" href="{expected_pt_url}">' in pt_text, f"Canonical PT incorreto em {slug_pt}"
        
        assert f'<link rel="alternate" hreflang="en" href="{expected_en_url}">' in en_text
        assert f'<link rel="alternate" hreflang="pt-BR" href="{expected_pt_url}">' in en_text
        assert f'<link rel="alternate" hreflang="x-default" href="{expected_en_url}">' in en_text
        
        assert f'<link rel="alternate" hreflang="en" href="{expected_en_url}">' in pt_text
        assert f'<link rel="alternate" hreflang="pt-BR" href="{expected_pt_url}">' in pt_text
        assert f'<link rel="alternate" hreflang="x-default" href="{expected_en_url}">' in pt_text
        
        assert '"inLanguage": "en"' in en_text, f"Schema inLanguage EN incorreto em {slug_en}"
        assert '"inLanguage": "pt-BR"' in pt_text, f"Schema inLanguage PT incorreto em {slug_pt}"
        
        tested_pairs += 1
        
    assert tested_pairs >= 8, f"Esperado >= 8 pares de hreflang testados, verificado {tested_pairs}"
    print(f"PASS: Gate 3 Reciprocidade de Hreflang e Canonicals Validados em {tested_pairs} pares")

def test_i18n_gate_4_no_broken_links_in_pt():
    pt_htmls = list((SITE_DIR / "pt").glob("**/*.html"))
    assert len(pt_htmls) > 0, "Nenhum HTML compilado em site/pt/"
    
    missing_targets = []
    cross_leaks = []
    for h in pt_htmls:
        html = h.read_text(encoding="utf-8")
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)
        for target in hrefs:
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#") or target.startswith("mailto:"):
                continue
            clean_target = target.split("#")[0].split("?")[0]
            if not clean_target:
                continue
            
            # Detect unwanted leakage to english blog posts from portuguese content body
            if "/blog/post/" in clean_target:
                cross_leaks.append(f"{h.name} -> {target}")
                
            if clean_target.startswith("/"):
                rel = clean_target.lstrip("/")
                if rel.startswith("blog/"):
                    rel = rel[5:]
                target_path = (SITE_DIR / rel).resolve()
            else:
                target_path = (h.parent / clean_target).resolve()
                
            if not target_path.exists() and not (target_path / "index.html").exists():
                missing_targets.append(f"{h.name} -> {target}")
                
    assert len(missing_targets) == 0, f"Links quebrados em PT: {missing_targets[:5]}"
    assert len(cross_leaks) == 0, f"Vazamentos de links em ingles em PT: {cross_leaks[:5]}"
    print(f"PASS: Gate 4 Links internos de site/pt/ 100% resolvidos e sem vazamento de idioma ({len(pt_htmls)} paginas)")

if __name__ == "__main__":
    print("=== INICIANDO VALIDACAO DA ESPECIFICACAO I18N ===")
    try:
        test_i18n_gate_1_routes_map()
        test_i18n_gate_2_pt_frontmatter_and_no_parentheses()
        test_i18n_gate_3_hreflang_and_canonical()
        test_i18n_gate_4_no_broken_links_in_pt()
        print("=== TODAS AS ASSERCOES I18N PASSARAM COM SUCESSO ===")
    except AssertionError as e:
        print(f"\n[FALHA DE ESPECIFICACAO I18N] {e}")
        sys.exit(1)
