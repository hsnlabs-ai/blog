#!/usr/bin/env python3
import re
from pathlib import Path

docs_pt = Path("/Users/hugosoares/blog_hsn_labs/docs/pt")

for f in docs_pt.rglob("*.md"):
    content = f.read_text(encoding="utf-8")
    original = content
    content = content.replace("Ler Ensaio &rarr;", "Ler Post &rarr;")
    content = content.replace("## Recursos Estrategicos e Ensaios Relacionados", "## Recursos Estrategicos e Posts Relacionados")
    content = content.replace("este ensaio", "este post")
    content = content.replace("Este ensaio", "Este post")
    content = content.replace("neste ensaio", "neste post")
    content = content.replace("Neste ensaio", "Neste post")
    content = content.replace("Ensaios", "Posts")
    content = content.replace("ensaios", "posts")
    content = content.replace("Ensaio", "Post")
    content = content.replace("ensaio", "post")
    
    if content != original:
        f.write_text(content, encoding="utf-8")
        print(f"Atualizado: {f.name}")

print("Concluida substituicao de ensaio por post em docs/pt/")
