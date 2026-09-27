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
    "Arquitetura e Engenharia Determinística",
    "Economia Agêntica e Fim do BPO",
    "Linha de Frente e Estudos de Caso"
}

def test_d1_frontmatter_schema():
    posts = sorted(glob.glob(str(POSTS_DIR / "*.md")))
    assert len(posts) == 19, f"Esperado 19 posts em docs/post, encontrado {len(posts)}"
    
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
        assert author == "Hugo Nascimento", f"Post {p} autor incorreto: {author}"
    print("PASS: Gate D1 Frontmatter Schema Validado nos 19 posts")

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

if __name__ == "__main__":
    print("=== INICIANDO EXECUCAO DA SUITE DE ESPECIFICACAO ===")
    try:
        test_d1_frontmatter_schema()
        test_d2_forbidden_pages_purged()
        test_d3_mkdocs_strict_build()
        test_d4_search_index_integrity()
        test_d5_internal_links()
        print("=== TODAS AS ASSERCOES PASSARAM COM SUCESSO ===")
    except AssertionError as e:
        print(f"FALHA DETERMINISTICA NO GATE: {e}", file=sys.stderr)
        sys.exit(1)
