#!/usr/bin/env python3
import re
import sys
from pathlib import Path

SITE_DIR = Path("/Users/hugosoares/site_hsn_labs")
BLOG_DIR = Path("/Users/hugosoares/blog_hsn_labs")

def test_gate_e1_cross_navigation():
    print("--- Gate E1: Integridade de Navegacao Cruzada ---")
    header_html = (BLOG_DIR / "overrides" / "modules" / "header.html").read_text(encoding="utf-8")
    assert "https://hsnlabs.ai/bootcamp/" in header_html, "CTA do header PT no blog deve apontar para /bootcamp/"
    assert "https://hsnlabs.ai/" in header_html, "Logo do header PT no blog deve apontar para /"

    footer_html = (BLOG_DIR / "overrides" / "modules" / "footer.html").read_text(encoding="utf-8")
    assert "https://hsnlabs.ai/bootcamp/" in footer_html, "Link do footer PT no blog deve apontar para /bootcamp/"
    assert "https://hsnlabs.ai/privacy-policy/" in footer_html, "Link de privacidade PT no blog deve apontar para /privacy-policy/"
    assert "pt/post/cemiterio-de-pocs/" in footer_html, "Pilares do footer PT no blog devem apontar para pt/post/"

    site_pt_index = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    assert '<li><a href="/bootcamp/">Agentic Bootcamp</a></li>' in site_pt_index
    assert '<li><a href="/advisory/">Advisory</a></li>' in site_pt_index
    assert '<li><a href="/blog/pt/">Blog</a></li>' in site_pt_index
    assert '<a href="/privacy-policy/">Política de Privacidade</a>' in site_pt_index
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

def test_gate_e3_llms_txt_endpoints():
    print("--- Gate E3: Validacao de Endpoints no llms.txt ---")
    llms_site = (SITE_DIR / "llms.txt").read_text(encoding="utf-8")
    assert "/blog/writing/" not in llms_site, "Rota antiga /blog/writing/ ainda presente no llms.txt do site"
    assert "/blog/post/" in llms_site, "Rota real /blog/post/ ausente no llms.txt do site"
    assert "https://hsnlabs.ai/databricks/" in llms_site, "Rota Databricks ausente no llms.txt do site"
    assert "https://hsnlabs.ai/blog/pt/" in llms_site, "Blog PT ausente no llms.txt do site"
    print("PASS: Gate E3 Endpoints de agentes e LLMs validados")

def test_gate_e4_zero_parentheses():
    print("--- Gate E4: Invariante Estrito Zero Parenteses ---")
    for f in (BLOG_DIR / "docs" / "pt").rglob("*.md"):
        txt = f.read_text(encoding="utf-8")
        c = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', txt)
        c = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', c)
        lines = [line.strip() for line in c.split('\n') if '(' in line or ')' in line]
        assert len(lines) == 0, f"Parentese em {f.name}: {lines}"
    print("PASS: Gate E4 Invariante Zero Parenteses auditado e validado em 100% dos textos PT")

if __name__ == "__main__":
    print("=== INICIANDO EXECUCAO DA SUITE ECOSSISTEMA hsnlabs ===")
    test_gate_e1_cross_navigation()
    test_gate_e2_essay_term_extinction()
    test_gate_e3_llms_txt_endpoints()
    test_gate_e4_zero_parentheses()
    print("=== TODAS AS ASSERCOES DO ECOSSISTEMA PASSARAM COM SUCESSO ===")
