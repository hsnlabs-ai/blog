import os
import re
import sys
import glob
import yaml
import json
import subprocess
import urllib.parse
from pathlib import Path

BASE_DIR = Path("/Users/hugosoares/blog_hsn_labs")
DOCS_DIR = BASE_DIR / "docs"
POSTS_DIR = DOCS_DIR / "post"
SITE_DIR = BASE_DIR / "site"

CANONICAL_CATEGORIES = {
    "Why Agents Fail",
    "Agent Development Life Cycle",
    "Future of Work",
    "Agentic Economics",
    "Case Studies"
}

def test_d1_frontmatter_schema():
    posts = sorted(glob.glob(str(POSTS_DIR / "*.md")))
    assert len(posts) >= 19, f"Esperado >= 19 posts em docs/post, encontrado {len(posts)}"
    
    for p in posts:
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        parts = content.split("---")
        assert len(parts) >= 3, f"Post {p} sem bloco frontmatter YAML valido"
        
        meta = yaml.safe_load(parts[1])
        assert isinstance(meta, dict), f"Post {p} com frontmatter corrompido"
        
        title = meta.get("title")
        assert title and isinstance(title, str) and 10 <= len(title) <= 130, f"Post {p} titulo invalido: {title}"
        
        date = str(meta.get("date"))
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", date), f"Post {p} data invalida: {date}"
        
        category = meta.get("category")
        assert category in CANONICAL_CATEGORIES, f"Post {p} categoria invalida: {category}"
        
        tags = meta.get("tags")
        assert isinstance(tags, list) and len(tags) >= 1, f"Post {p} tags invalidas: {tags}"
        for t in tags:
            assert re.match(r"^[a-z0-9\-]+$", str(t)), f"Post {p} tag fora do padrao: {t}"
            
        desc = meta.get("description")
        assert desc and isinstance(desc, str) and 30 <= len(desc) <= 200, f"Post {p} descricao fora do limite: {desc}"
        
        author = meta.get("author")
        assert author == "Hugo S. Nascimento", f"Post {p} autor incorreto: {author}"
    print(f"PASS: Gate D1 Frontmatter Schema Validado nos {len(posts)} posts")

def test_d2_forbidden_pages_purged():
    user_manual = DOCS_DIR / "about" / "user-manual.md"
    services = DOCS_DIR / "services.md"
    assert not user_manual.exists(), "ERRO: docs/about/user-manual.md ainda existe"
    assert not services.exists(), "ERRO: docs/services.md ainda existe"
    print("PASS: Gate D2 Paginas Proibidas Eliminadas")

def test_d3_mkdocs_strict_build():
    cmd = ["uv", "run", "mkdocs", "build", "--strict"]
    res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"Build falhou com codigo {res.returncode}:\n{res.stderr}\n{res.stdout}"
    print("PASS: Gate D3 Build Estrito Concluido sem erros")

def test_d4_search_index_integrity():
    search_file = SITE_DIR / "search" / "search_index.json"
    assert search_file.exists(), "Indice de busca nao encontrado"
    with open(search_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    docs = data.get("docs", [])
    assert len(docs) >= 19, f"Indice com apenas {len(docs)} documentos, esperado >= 19"
    print("PASS: Gate D4 Indice de Busca Integra com 19+ documentos")

def test_d5_internal_links():
    html_files = list(SITE_DIR.glob("**/*.html"))
    assert len(html_files) > 0, "Nenhum arquivo HTML compilado encontrado"
    
    missing_targets = []
    for h in html_files:
        with open(h, "r", encoding="utf-8") as f:
            html = f.read()
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)
        for target in hrefs:
            if target.startswith("http://") or target.startswith("https://") or target.startswith("#") or target.startswith("mailto:"):
                continue
            clean_target = urllib.parse.unquote(target.split("#")[0].split("?")[0])
            if not clean_target:
                continue
            if clean_target.startswith("/"):
                # Absolute to site root
                target_path = (SITE_DIR / clean_target.lstrip("/")).resolve()
            else:
                target_path = (h.parent / clean_target).resolve()
            if not target_path.exists() and not (target_path / "index.html").exists():
                missing_targets.append(f"{h.name} -> {target}")
                
    assert len(missing_targets) == 0, f"Links quebrados encontrados: {missing_targets[:5]}"
    print("PASS: Gate D5 Todos os links internos sao validos")

def test_d6_rss_feed():
    rss_file = SITE_DIR / "feed_rss_created.xml"
    json_feed = SITE_DIR / "feed_json_created.json"
    assert rss_file.exists(), "ERRO: feed_rss_created.xml nao gerado"
    assert json_feed.exists(), "ERRO: feed_json_created.json nao gerado"
    
    # Assert valid well-formed XML and valid image URL
    import xml.etree.ElementTree as ET
    tree = ET.parse(rss_file)
    root = tree.getroot()
    channel = root.find('channel')
    assert channel is not None, "ERRO: channel ausente no XML do RSS"
    image = channel.find('image')
    assert image is not None, "ERRO: tag image ausente no canal RSS"
    url_tag = image.find('url')
    assert url_tag is not None, "ERRO: tag url ausente em image"
    image_url = url_tag.text
    assert image_url and image_url != "None" and image_url.startswith("http"), f"ERRO: URL de imagem invalida no RSS: {image_url}"
    
    with open(rss_file, "r", encoding="utf-8") as f:
        rss_content = f.read()
    item_count = len(re.findall(r"<item>", rss_content))
    assert item_count >= 19, f"RSS com apenas {item_count} items, esperado >= 19"
    print("PASS: Gate D6 RSS Feed e JSON Feed gerados, validos como XML estrito e com logo oficial")

def test_d7_robots_and_sitemap():
    robots_file = SITE_DIR / "robots.txt"
    assert robots_file.exists(), "ERRO: site/robots.txt nao existe"
    with open(robots_file, "r", encoding="utf-8") as f:
        robots_txt = f.read()
    assert "Sitemap: https://hsnlabs.ai/blog/sitemap.xml" in robots_txt, "robots.txt sem declaracao de sitemap"
    
    sitemap_file = SITE_DIR / "sitemap.xml"
    assert sitemap_file.exists(), "ERRO: site/sitemap.xml nao existe"
    with open(sitemap_file, "r", encoding="utf-8") as f:
        sitemap_xml = f.read()
    assert "<loc>https://hsnlabs.ai/blog/post/why-rag-breaks-on-erp/</loc>" in sitemap_xml, "sitemap.xml incompleto"
    print("PASS: Gate D7 robots.txt e sitemap.xml integros")

def test_d8_pagination_contract():
    index_file = SITE_DIR / "index.html"
    with open(index_file, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="blog-pagination"' in html or 'class="blog-pagination"' in html, "ERRO: Container de paginacao ausente em index.html"
    assert 'data-page-size="10"' in html or 'data-posts-per-page="10"' in html or 'pagination-btn' in html, "ERRO: Controles de paginacao de 10 artigos ausentes"
    print("PASS: Gate D8 Paginacao de 10 artigos por pagina configurada")

def test_d9_head_seo_meta():
    index_file = SITE_DIR / "index.html"
    with open(index_file, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'rel="alternate" type="application/rss+xml"' in html, "ERRO: Tag link de RSS Feed ausente no head"
    assert 'application/ld+json' in html or 'property="og:title"' in html, "ERRO: Metatags OpenGraph ou Schema JSON-LD ausentes"
    print("PASS: Gate D9 Metatags de Indexacao e SEO presentes no head")

def test_d10_replicated_footer():
    index_file = SITE_DIR / "index.html"
    with open(index_file, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'class="site-footer"' in html, "ERRO: site-footer ausente no HTML"
    assert 'São Paulo' in html and 'WeWork' in html, "ERRO: Informacoes de localizacao ausentes no footer"
    assert 'Why Agents Fail' in html, "ERRO: Pilar Why Agents Fail ausente no footer"
    assert 'Agent Development Life Cycle' in html, "ERRO: Pilar Agent Development Life Cycle ausente no footer"
    assert 'Future of Work' in html, "ERRO: Pilar Future of Work ausente no footer"
    assert 'Agentic Economics' in html, "ERRO: Pilar Agentic Economics ausente no footer"
    assert 'Case Studies' in html, "ERRO: Pilar Case Studies ausente no footer"
    assert 'llms.txt for LLMs & Agents' in html, "ERRO: Link llms.txt ausente no footer"
    assert '2026 HSN Labs' in html, "ERRO: Copyright ausente no footer"
    print("PASS: Gate D10 Footer minimalista com pilares de indexacao e SEO validado")

def test_d11_brand_typography_and_colors():
    css_file = SITE_DIR / "stylesheets/extra.css"
    assert css_file.exists(), "ERRO: stylesheets/extra.css nao compilado no site"
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()
    assert 'Cormorant Garamond' in css, "ERRO: Tipografia Cormorant Garamond ausente no CSS"
    assert 'Inter' in css, "ERRO: Tipografia Inter ausente no CSS"
    assert '--cyan: #52B4FD' in css or '--cyan:' in css, "ERRO: Token de cor Brand Cyan ausente"
    print("PASS: Gate D11 Cores e tipografia institucionais HSN Labs ativas")

def test_d12_geo_indexnow_and_websub():
    indexnow_file = SITE_DIR / "fb6d944d28fc4484bd669f6d9c4d3292.txt"
    assert indexnow_file.exists(), "ERRO: Arquivo de chave IndexNow ausente no site build"
    
    llms_file = SITE_DIR / "llms.txt"
    assert llms_file.exists(), "ERRO: llms.txt ausente no site build"
    
    index_file = SITE_DIR / "index.html"
    with open(index_file, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'name="geo.region" content="BR-SP"' in html, "ERRO: Meta tag GEO region ausente"
    assert 'name="geo.placename" content="São Paulo"' in html, "ERRO: Meta tag GEO placename ausente"
    assert 'name="msvalidate.01"' in html, "ERRO: Meta tag msvalidate Bing ausente"
    
    rss_file = SITE_DIR / "feed_rss_created.xml"
    with open(rss_file, "r", encoding="utf-8") as f:
        rss = f.read()
    assert 'hub="https://pubsubhubbub.appspot.com/"' in rss or 'rel="hub"' in rss, "ERRO: WebSub hub ausente no feed RSS"
    print("PASS: Gate D12 GEO, Bing IndexNow e WebSub Hub validados com sucesso")

def test_d13_zero_portuguese_policy():
    index_file = SITE_DIR / "index.html"
    with open(index_file, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Verify HOME header is absent from homepage
    assert 'id="component-title">Home</h1>' not in html, "ERRO: Header Home nao removido da homepage"
    assert '<p class="page-dates">' not in html, "ERRO: Data automatica page-dates nao removida da homepage"
    
    # Verify zero Portuguese strings in index.html
    pt_tokens = ['artigo', 'artigos', 'pagina anterior', 'proxima pagina', 'mostrando artigos', 'ensaios & notas']
    for token in pt_tokens:
        assert token not in html.lower(), f"ERRO: Token em portugues '{token}' encontrado em index.html"
    print("PASS: Gate D13 Zero Portuguese policy e remocao de header Home validados")

if __name__ == "__main__":
    print("=== INICIANDO EXECUCAO DA SUITE DE ESPECIFICACAO ===")
    try:
        test_d1_frontmatter_schema()
        test_d2_forbidden_pages_purged()
        test_d3_mkdocs_strict_build()
        test_d4_search_index_integrity()
        test_d5_internal_links()
        test_d6_rss_feed()
        test_d7_robots_and_sitemap()
        test_d8_pagination_contract()
        test_d9_head_seo_meta()
        test_d10_replicated_footer()
        test_d11_brand_typography_and_colors()
        test_d12_geo_indexnow_and_websub()
        test_d13_zero_portuguese_policy()
        print("=== TODAS AS ASSERCOES PASSARAM COM SUCESSO ===")
    except AssertionError as e:
        print(f"\n[FALHA DE ESPECIFICACAO] {e}")
        sys.exit(1)
