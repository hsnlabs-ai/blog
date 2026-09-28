import json
import re
import unicodedata
from pathlib import Path
from collections import defaultdict, Counter

DICT_PATH = Path("/Users/hugosoares/blog_hsn_labs/scripts/br-utf8.txt")
BASE_DIR = Path("/Users/hugosoares/blog_hsn_labs")
PT_DIR = BASE_DIR / "docs" / "pt"
SCRIPTS_DIR = BASE_DIR / "scripts"

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Load dictionary
raw_dict = DICT_PATH.read_text(encoding="utf-8").splitlines()
accent_map = defaultdict(set)
valid_dictionary_words = set()

for line in raw_dict:
    w = line.strip()
    if not w:
        continue
    w_low = w.lower()
    valid_dictionary_words.add(w_low)
    stripped = strip_accents(w_low)
    accent_map[stripped].add(w_low)

# Technical whitelist (do not treat as Portuguese words needing accents)
WHITELIST = {
    "twenty", "bpo", "crm", "erp", "mcp", "pydantic", "python", "ai", "llm", "rag",
    "prompt", "prompts", "blueprint", "stack", "stacks", "saas", "ebitda", "roi",
    "latam", "airlines", "cleveland", "clinic", "palantir", "aip", "databricks",
    "lakehouse", "data", "hub", "spoke", "framework", "c-suite", "ceo", "cfo", "cio",
    "cpto", "poc", "pocs", "code", "cases", "case", "studies", "economics", "adlc",
    "eval", "evals", "benchmark", "benchmarks", "sql", "vector", "state", "machines",
    "kafka", "loops", "loop", "api", "apis", "schema", "schemas", "drift", "guardrails",
    "post", "posts", "blog", "bootcamp", "advisory", "deloitte", "santander", "softplan",
    "unipar", "carbocloro", "lwsa", "turbi", "caju", "cast", "group", "insi", "eva",
    "people", "hsn", "labs", "linkedin", "github", "versus", "vs", "status", "active",
    "guidelines", "english", "version", "offline", "online", "setup", "sla", "slas"
}

# Scan files
files_to_scan = list(PT_DIR.glob("**/*.md"))
files_to_scan.append(SCRIPTS_DIR / "generate_pt_index.py")

audit_results = {
    "deterministic": defaultdict(lambda: {"count": 0, "target": "", "occurrences": []}),
    "ambiguous": defaultdict(lambda: {"count": 0, "targets": [], "occurrences": []}),
    "unrecognized": defaultdict(lambda: {"count": 0, "occurrences": []})
}

def match_case(original, replacement):
    if original.isupper():
        return replacement.upper()
    elif original.istitle():
        return replacement.capitalize()
    return replacement

for fpath in files_to_scan:
    rel_path = str(fpath.relative_to(BASE_DIR))
    lines = fpath.read_text(encoding="utf-8").splitlines()
    in_code_block = False
    
    for l_idx, line in enumerate(lines, start=1):
        # Handle code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
            
        # Clean line for token checking: strip code spans and link URLs
        cleaned_line = re.sub(r'`.*?`', ' ', line)
        cleaned_line = re.sub(r'\]\([^)]+\)', '] ', cleaned_line)
        cleaned_line = re.sub(r'href="[^"]+"', ' ', cleaned_line)
        
        # Tokenize words
        tokens = re.finditer(r'\b[a-zA-ZáéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇàÀèÈìÌòÒùÙüÜ-]+\b', cleaned_line)
        for match in tokens:
            token = match.group(0)
            token_low = token.lower()
            token_strip = strip_accents(token_low)
            
            if token_low in WHITELIST or token_strip in WHITELIST:
                continue
            if len(token) <= 1 and token_low not in ["e", "a"]:
                continue
                
            # If word is already accented and in dictionary, it's valid
            if token_low in valid_dictionary_words and token_low != token_strip:
                continue
                
            # Check dictionary variants for this unaccented root
            candidates = accent_map.get(token_strip, set())
            
            # If stripped token has accented alternatives in dictionary
            accented_candidates = {c for c in candidates if c != token_strip}
            
            if not accented_candidates:
                continue
                
            # Categorize
            if token_low not in valid_dictionary_words:
                # Token itself is NOT a valid word without accent in Portuguese!
                # Deterministic fix!
                if len(accented_candidates) == 1:
                    target = list(accented_candidates)[0]
                    res = audit_results["deterministic"][token]
                    res["count"] += 1
                    res["target"] = match_case(token, target)
                    res["occurrences"].append({"file": rel_path, "line": l_idx})
                else:
                    # Multiple accented options (e.g. critica -> crítica, criticá)
                    # Filter out obscure verb forms ending in stressed vowels if common noun exists
                    pref = [c for c in accented_candidates if not c.endswith(('á', 'é', 'í', 'ó', 'ú'))]
                    target = pref[0] if len(pref) == 1 else sorted(list(accented_candidates))[0]
                    res = audit_results["deterministic"][token]
                    res["count"] += 1
                    res["target"] = match_case(token, target)
                    res["occurrences"].append({"file": rel_path, "line": l_idx})
            else:
                # Token IS a valid word even unaccented (e.g., e / é, esta / está, pelo / pêlo)
                res = audit_results["ambiguous"][token]
                res["count"] += 1
                res["targets"] = [match_case(token, c) for c in accented_candidates]
                res["occurrences"].append({"file": rel_path, "line": l_idx, "context": line.strip()[:80]})

# Write output json
output_path = SCRIPTS_DIR / "accent_audit_report.json"
with open(output_path, "w", encoding="utf-8") as out:
    json.dump(audit_results, out, ensure_ascii=False, indent=2)

print("AUDIT FINISHED")
print(f"Deterministic distinct tokens: {len(audit_results['deterministic'])}")
total_det_instances = sum(item["count"] for item in audit_results["deterministic"].values())
print(f"Total deterministic occurrences: {total_det_instances}")

print(f"Ambiguous distinct tokens: {len(audit_results['ambiguous'])}")
total_amb_instances = sum(item["count"] for item in audit_results["ambiguous"].values())
print(f"Total ambiguous occurrences: {total_amb_instances}")

# Top 20 deterministic corrections
print("\nTOP 20 DETERMINISTIC CORRECTIONS:")
sorted_det = sorted(audit_results["deterministic"].items(), key=lambda x: x[1]["count"], reverse=True)
for word, data in sorted_det[:20]:
    print(f"  {word} -> {data['target']} ({data['count']}x)")

print("\nAMBIGUOUS TOKENS:")
sorted_amb = sorted(audit_results["ambiguous"].items(), key=lambda x: x[1]["count"], reverse=True)
for word, data in sorted_amb:
    print(f"  {word} ({data['count']}x) -> options: {data['targets']}")
