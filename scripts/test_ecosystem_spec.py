#!/usr/bin/env python3
import re
import sys
from pathlib import Path

SITE_DIR = Path("/Users/hugosoares/site_hsn_labs")
BLOG_DIR = Path("/Users/hugosoares/blog_hsn_labs")

def test_gate_e1_cross_navigation():
    print("--- Gate E1: Integridade de Navegacao Cruzada ---")
    # 1. Check blog PT header
    header_html = (BLOG_DIR / "overrides" / "modules" / "header.html").read_text(encoding="utf-8")
    assert "https://hsnlabs.ai/pt/bootcamp" in header_html, "CTA do header PT no blog deve apontar para /pt/bootcamp"
    assert "https://hsnlabs.ai/pt/" in header_html, "Logo do header PT no blog deve apontar para /pt/"
    
    # 2. Check blog PT footer
    footer_html = (BLOG_DIR / "overrides" / "modules" / "footer.html").read_text(encoding="utf-8")
    assert "https://hsnlabs.ai/pt/bootcamp" in footer_html, "Link do footer PT no blog deve apontar para /pt/bootcamp"
    assert "https://hsnlabs.ai/pt/privacy-policy" in footer_html, "Link de privacidade PT no blog deve apontar para /pt/privacy-policy"
    assert "pt/post/cemiterio-de-pocs/" in footer_html, "Pilares do footer PT no blog devem apontar para pt/post/"
    
    # 3. Check site PT footer navigation
    site_pt_index = (SITE_DIR / "pt" / "index.html").read_text(encoding="utf-8")
    assert '<li><a href="/pt/bootcamp/">Bootcamp de Agentes</a></li>' in site_pt_index, "Menu footer site PT deve apontar para /pt/bootcamp/"
    assert '<li><a href="/pt/advisory/">Advisory</a></li>' in site_pt_index, "Menu footer site PT deve apontar para /pt/advisory/"
    assert '<li><a href="/blog/pt/">Blog</a></li>' in site_pt_index, "Menu footer site PT deve apontar para /blog/pt/"
    assert '<a href="/pt/privacy-policy/">Politica de Privacidade</a>' in site_pt_index, "Link de privacidade no footer do site PT deve apontar para /pt/privacy-policy/"
    print("PASS: Gate E1 Navegacao Cruzada validada sem vazamento de idioma")

def test_gate_e2_essay_term_extinction():
    print("--- Gate E2: Extincao do Termo Ensaio ---")
    pt_docs = list((BLOG_DIR / "docs" / "pt").rglob("*.md"))
    assert len(pt_docs) >= 15, "Menos de 15 documentos PT encontrados"
    for f in pt_docs:
        content = f.read_text(encoding="utf-8")
        matches = re.findall(r'\b(ensaio|ensaios)\b', content, re.IGNORECASE)
        assert len(matches) == 0, f"Termo ensaio ainda encontrado em {f.name}: {matches}"
    print(f"PASS: Gate E2 Termo ensaio eliminado com sucesso em todos os {len(pt_docs)} arquivos PT do blog")

def test_gate_e3_lgpd_banner():
    print("--- Gate E3: Consistencia do Banner LGPD ---")
    pt_pages = list((SITE_DIR / "pt").glob("**/index.html"))
    assert len(pt_pages) == 6, f"Esperadas 6 paginas PT no site, encontradas {len(pt_pages)}"
    for p in pt_pages:
        content = p.read_text(encoding="utf-8")
        assert "Consentimento de Privacidade e Cookies" in content, f"Titulo LGPD ausente em {p}"
        assert 'href="/pt/privacy-policy/"' in content, f"Link para /pt/privacy-policy/ ausente no banner LGPD de {p}"
        assert "Aceitar Todos" in content, f"Botao Aceitar Todos ausente em {p}"
        assert "Recusar" in content, f"Botao Recusar ausente em {p}"
    print(f"PASS: Gate E3 Banner LGPD e Politica de Privacidade validados nas {len(pt_pages)} paginas PT do site")

def test_gate_e4_llms_txt_endpoints():
    print("--- Gate E4: Validacao de Endpoints no llms.txt ---")
    llms_site = (SITE_DIR / "llms.txt").read_text(encoding="utf-8")
    assert "/blog/writing/" not in llms_site, "Rota antiga /blog/writing/ ainda presente no llms.txt do site"
    assert "/blog/post/" in llms_site, "Rota real /blog/post/ ausente no llms.txt do site"
    assert "https://hsnlabs.ai/pt/" in llms_site, "Secao PT ausente no llms.txt do site"
    assert "https://hsnlabs.ai/blog/pt/" in llms_site, "Blog PT ausente no llms.txt do site"
    print("PASS: Gate E4 Endpoints de agentes e LLMs validados")

def test_gate_e5_zero_parentheses():
    print("--- Gate E5: Invariante Estrito Zero Parenteses ---")
    # Test blog PT markdown
    for f in (BLOG_DIR / "docs" / "pt").rglob("*.md"):
        txt = f.read_text(encoding="utf-8")
        c = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', txt)
        c = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', c)
        lines = [line.strip() for line in c.split('\n') if '(' in line or ')' in line]
        assert len(lines) == 0, f"Parentese em {f.name}: {lines}"
    
    # Test site PT pages text
    for f in (SITE_DIR / "pt").glob("**/index.html"):
        txt = f.read_text(encoding="utf-8")
        c = re.sub(r'<style.*?</style>', '', txt, flags=re.DOTALL | re.IGNORECASE)
        c = re.sub(r'<script.*?</script>', '', c, flags=re.DOTALL | re.IGNORECASE)
        c = re.sub(r'<svg.*?</svg>', '', c, flags=re.DOTALL | re.IGNORECASE)
        c = re.sub(r'style="[^"]*"', '', c)
        text_nodes = re.findall(r'>([^<]+)<', c)
        for t in text_nodes:
            s = t.strip()
            if not s: continue
            assert '(' not in s and ')' not in s, f"Parentese encontrado no texto visivel de {f}: {s}"
    print("PASS: Gate E5 Invariante Zero Parenteses auditado e validado em 100% dos textos PT")

if __name__ == "__main__":
    print("=== INICIANDO EXECUCAO DA SUITE ECOSSISTEMA HSN LABS ===")
    test_gate_e1_cross_navigation()
    test_gate_e2_essay_term_extinction()
    test_gate_e3_lgpd_banner()
    test_gate_e4_llms_txt_endpoints()
    test_gate_e5_zero_parentheses()
    print("=== TODAS AS ASSERCOES DO ECOSSISTEMA PASSARAM COM SUCESSO ===")
