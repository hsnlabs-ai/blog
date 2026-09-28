import json
import re
from pathlib import Path
import subprocess

BASE_DIR = Path("/Users/hugosoares/blog_hsn_labs")
PT_POSTS_DIR = BASE_DIR / "docs" / "pt" / "post"
LLMS_TXT = BASE_DIR / "docs" / "llms.txt"
REPORT_PATH = BASE_DIR / "scripts" / "accent_audit_report.json"

# Load deterministic dictionary
data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
replacements = {}
for word, info in data["deterministic"].items():
    replacements[word] = info["target"]

# Add reviewed domain words
domain_words = {
    "negocio": "negócio", "Negocio": "Negócio", "negocios": "negócios", "Negocios": "Negócios",
    "maquinas": "máquinas", "Maquinas": "Máquinas", "maquina": "máquina", "Maquina": "Máquina",
    "credito": "crédito", "Credito": "Crédito", "debito": "débito", "Debito": "Débito",
    "lideres": "líderes", "Lideres": "Líderes",
    "analise": "análise", "Analise": "Análise", "analises": "análises", "Analises": "Análises",
    "criticas": "críticas", "Criticas": "Críticas", "critico": "crítico", "Critico": "Crítico",
    "critica": "crítica", "Critica": "Crítica", "criticos": "críticos", "Criticos": "Críticos",
    "politica": "política", "Politica": "Política", "politicas": "políticas", "Politicas": "Políticas",
    "ate": "até", "Ate": "Até",
    "pratica": "prática", "Pratica": "Prática", "pratico": "prático", "Pratico": "Prático",
    "praticas": "práticas", "Praticas": "Práticas", "praticos": "práticos", "Praticos": "Práticos",
    "peca": "peça", "Peca": "Peça", "pecas": "peças", "Pecas": "Peças",
    "forca": "força", "Forca": "Força", "forcas": "forças", "Forcas": "Forças",
    "duvida": "dúvida", "Duvida": "Dúvida", "duvidas": "dúvidas", "Duvidas": "Dúvidas",
    "modulo": "módulo", "Modulo": "Módulo", "modulos": "módulos", "Modulos": "Módulos",
    "veiculo": "veículo", "Veiculo": "Veículo", "veiculos": "veículos", "Veiculos": "Veículos",
    "catalogo": "catálogo", "Catalogo": "Catálogo",
    "privilegio": "privilégio", "Privilegio": "Privilégio",
    "ruido": "ruído", "Ruido": "Ruído",
    "rotulo": "rótulo", "Rotulo": "Rótulo",
    "esforco": "esforço", "Esforco": "Esforço",
    "beneficio": "benefício", "Beneficio": "Benefício", "beneficios": "benefícios", "Beneficios": "Benefícios",
    "bancaria": "bancária", "Bancaria": "Bancária", "bancarias": "bancárias", "Bancarias": "Bancárias",
    "bancario": "bancário", "Bancario": "Bancário", "bancarios": "bancários", "Bancarios": "Bancários",
    "tributaria": "tributária", "Tributaria": "Tributária", "tributarias": "tributárias", "Tributarias": "Tributárias",
    "medica": "médica", "Medica": "Médica", "medico": "médico", "Medico": "Médico",
    "medicas": "médicas", "Medicas": "Médicas", "medicos": "médicos", "Medicos": "Médicos",
    "clinica": "clínica", "Clinica": "Clínica", "clinicas": "clínicas", "Clinicas": "Clínicas",
    "paginas": "páginas", "Paginas": "Páginas",
    "sequencia": "sequência", "Sequencia": "Sequência",
    "distancia": "distância", "Distancia": "Distância",
    "evidencias": "evidências", "Evidencias": "Evidências",
    "referencia": "referência", "Referencia": "Referência",
    "diagnostico": "diagnóstico", "Diagnostico": "Diagnóstico",
    "valido": "válido", "Valido": "Válido", "valida": "válida", "Valida": "Válida",
    "validas": "válidas", "Validas": "Válidas", "validos": "válidos", "Validos": "Válidos",
    "liquido": "líquido", "Liquido": "Líquido", "liquida": "líquida", "Liquida": "Líquida",
    "publico": "público", "Publico": "Público", "publica": "pública", "Publica": "Pública",
    "publicas": "públicas", "Publicas": "Públicas", "publicos": "públicos", "Publicos": "Públicos",
    "explicito": "explícito", "Explicito": "Explícito", "explicita": "explícita", "Explicita": "Explícita",
    "explicitas": "explícitas", "Explicitas": "Explícitas",
    "especifico": "específico", "Especifico": "Específico", "especifica": "específica", "Especifica": "Específica",
    "especificos": "específicos", "especificas": "específicas",
    "historico": "histórico", "Historico": "Histórico", "historica": "histórica", "Historica": "Histórica",
    "matematica": "matemática", "Matematica": "Matemática", "matematico": "matemático", "Matematico": "Matemático",
    "matematicas": "matemáticas", "matematicos": "matemáticos",
    "cadencia": "cadência", "Cadencia": "Cadência",
    "fracionaria": "fracionária", "Fracionaria": "Fracionária",
    "periodo": "período", "Periodo": "Período",
    "criterio": "critério", "Criterio": "Critério", "criterios": "critérios", "Criterios": "Critérios",
    "cenario": "cenário", "Cenario": "Cenário", "cenarios": "cenários", "Cenarios": "Cenários",
    "usuario": "usuário", "Usuario": "Usuário", "usuarios": "usuários", "Usuarios": "Usuários",
    "remedio": "remédio", "Remedio": "Remédio",
    "patrimonio": "patrimônio", "Patrimonio": "Patrimônio",
    "dolar": "dólar", "Dolar": "Dólar", "dolares": "dólares", "Dolares": "Dólares",
    "inicio": "início", "Inicio": "Início",
    "dividas": "dívidas", "Dividas": "Dívidas",
    "assedio": "assédio", "Assedio": "Assédio",
    "pais": "país", "Pais": "País",
    "continuo": "contínuo", "Continuo": "Contínuo", "continua": "contínua", "Continua": "Contínua",
    "agencias": "agências", "Agencias": "Agências", "agencia": "agência", "Agencia": "Agência",
    "pericia": "perícia", "Pericia": "Perícia",
    "familia": "família", "Familia": "Família",
    "historia": "história", "Historia": "História",
    "intermediaria": "intermediária", "Intermediaria": "Intermediária",
    "intermediarias": "intermediárias", "Intermediarias": "Intermediárias",
    "intermediario": "intermediário", "Intermediario": "Intermediário",
    "intermediarios": "intermediários", "Intermediarios": "Intermediários"
}
replacements.update(domain_words)

sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
word_pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted_keys) + r')\b')

phrase_patterns = [
    (re.compile(r'\bO Que E\b'), 'O Que É'),
    (re.compile(r'\bEsta em Colapso\b'), 'Está em Colapso'),
    (re.compile(r'\bEles Sao\b'), 'Eles São'),
    (re.compile(r'\bnao e\b'), 'não é'),
    (re.compile(r'\bNao e\b'), 'Não é'),
    (re.compile(r'\bnao sao\b'), 'não são'),
    (re.compile(r'\bNao sao\b'), 'Não são'),
    (re.compile(r'\bEssa ponte e a\b'), 'Essa ponte é a'),
    (re.compile(r'\bO resultado e\b'), 'O resultado é'),
    (re.compile(r'\bontologia operacional e a\b'), 'ontologia operacional é a'),
    (re.compile(r'\bque e\b'), 'que é'),
    (re.compile(r'\be a unica\b'), 'é a única'),
    (re.compile(r'\be o unico\b'), 'é o único'),
    (re.compile(r'\be a peca\b'), 'é a peça'),
    (re.compile(r'\be o motor\b'), 'é o motor'),
    (re.compile(r'\be o reflexo\b'), 'é o reflexo'),
    (re.compile(r'\be inquestionavel\b'), 'é inquestionável'),
    (re.compile(r'\be ineficiente\b'), 'é ineficiente'),
    (re.compile(r'\be composto por\b'), 'é composto por'),
    (re.compile(r'\be software\b'), 'é software'),
    (re.compile(r'\be desenhado\b'), 'é desenhado'),
    (re.compile(r'\be chamado\b'), 'é chamado'),
    (re.compile(r'\bas 2 da Manha\b'), 'às 2 da Manhã'),
    (re.compile(r'\b2 da manha\b'), '2 da manhã'),
]

def replace_in_text(text):
    for pat, repl in phrase_patterns:
        text = pat.sub(repl, text)
    def _repl(match):
        return replacements.get(match.group(0), match.group(0))
    return word_pattern.sub(_repl, text)

def process_line(line):
    pattern = r'(`[^`]+`|(?<=\])\([^)]+\)|https?://[^\s)]+|<[^>]+>)'
    parts = []
    last_end = 0
    for match in re.finditer(pattern, line):
        start, end = match.span()
        if start > last_end:
            parts.append(replace_in_text(line[last_end:start]))
        parts.append(match.group(0))
        last_end = end
    if last_end < len(line):
        parts.append(replace_in_text(line[last_end:]))
    return ''.join(parts)

def process_file(file_path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    in_code_block = False
    in_frontmatter = False
    frontmatter_count = 0
    
    for line in lines:
        if line.strip() == "---":
            frontmatter_count += 1
            in_frontmatter = (frontmatter_count == 1)
            new_lines.append(line)
            continue
            
        if in_frontmatter and frontmatter_count == 1:
            if line.startswith("title:") or line.startswith("description:"):
                new_lines.append(process_line(line))
            else:
                new_lines.append(line)
            continue
            
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue
            
        new_lines.append(process_line(line))
        
    new_content = '\n'.join(new_lines) + ('\n' if content.endswith('\n') else '')
    if new_content != content:
        file_path.write_text(new_content, encoding="utf-8")
        return True
    return False

# Process all 31 posts
modified_count = 0
for post_file in sorted(PT_POSTS_DIR.glob("*.md")):
    if process_file(post_file):
        modified_count += 1

print(f"Posts modified: {modified_count} / {len(list(PT_POSTS_DIR.glob('*.md')))}")

# Process llms.txt if present
if LLMS_TXT.exists():
    llms_content = LLMS_TXT.read_text(encoding="utf-8")
    new_llms = '\n'.join(process_line(l) for l in llms_content.splitlines())
    if new_llms != llms_content:
        LLMS_TXT.write_text(new_llms + '\n', encoding="utf-8")
        print("llms.txt updated.")

# Regenerate docs/pt/index.md using generate_pt_index.py
gen_script = BASE_DIR / "scripts" / "generate_pt_index.py"
res = subprocess.run(["python3", str(gen_script)], capture_output=True, text=True)
print("generate_pt_index output:", res.stdout.strip())
