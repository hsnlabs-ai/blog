import os
import sys
import time
import json
import base64
from pathlib import Path
from google import genai

# Setup API Key
env_file = Path.home() / '.hermes/.env'
api_key = None
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if line.strip().startswith('GEMINI_API_KEY='):
            api_key = line.strip().split('=', 1)[1].strip('\"\'')
            break

if not api_key:
    api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

client = genai.Client(api_key=api_key)

STYLE_BASE = (
    "Tactile minimalist engineering aesthetic for HSN Labs. "
    "Deep dark obsidian background #07090E, charcoal #0E1017, crisp fine hairline cyan lines #52B4FD, "
    "clean geometric 90-degree boxes and architectural lines, subtle slate grey #94A3B8, "
    "no neon glow, no purple, no sci-fi slop, strict high-end engineering visual, 16:9 aspect ratio."
)

PROMPTS = {
    "autonomous-negotiations-collections-contracts": (
        f"{STYLE_BASE} Architectural schematic and conceptual representation of autonomous corporate collections and contract execution. "
        "A structured matrix of legal agreements and settlement balances in crisp cyan grids, automated algorithmic dispute resolution gates, "
        "precision ledger routing connecting enterprise counterparties without human intermediaries."
    ),
    "balance-sheet-guard-bpo-extinction": (
        f"{STYLE_BASE} Minimalist conceptual artwork of a balance sheet ledger scale. A massive dark slate block representing legacy BPO human services "
        "being mathematically displaced by a lightweight, sharp-edged cyan geometric prism representing autonomous agent execution. Sober financial austerity."
    ),
    "bpo-replacement-matrix": (
        f"{STYLE_BASE} Technical blueprint of the BPO Replacement Matrix. A 2D coordinate grid with axes 'Operational Latency' vs 'Cost per Transaction'. "
        "Sharp rectangular benchmark clusters comparing manual back-office human tiers with sub-second autonomous agent states in pure cyan #52B4FD."
    ),
    "c-suite-margin-protection-playbook": (
        f"{STYLE_BASE} Minimalist editorial conceptual visual of executive margin defense. An austere dark boardroom table in slate and obsidian, "
        "with an architectural model of expanding EBITDA margins protected by sharp geometric boundary walls in crisp cyan hairline vectors."
    ),
    "chatbot-vs-agent": (
        f"{STYLE_BASE} Technical architectural comparison diagram. Left side: a fragile, porous speech bubble fragmenting into unstable dotted lines (Chatbot). "
        "Right side: a monolithic, rock-solid rectangular state machine with deterministic database write locks and MCP verification perimeters in cyan (Agent)."
    ),
    "cleveland-clinic-case-study-operational-agents": (
        f"{STYLE_BASE} Technical healthcare systems blueprint. An architectural bird's-eye schematic of hospital bed management across 6,600 beds. "
        "Orthogonal corridor grids in slate grey with live bed capacity nodes connected by deterministic routing vectors in sky blue and emerald green."
    ),
    "collapse-of-legacy-rpa": (
        f"{STYLE_BASE} Conceptual artwork of crumbling brittle mechanics. Heavy, rigid mechanical gears and brittle UI-automation scripts shattering "
        "under structural tension, contrasted with a smooth, unyielding monolithic API bus and autonomous state machine in dark obsidian and sharp cyan."
    ),
    "cost-legacy-it": (
        f"{STYLE_BASE} Technical schematic of enterprise compute and risk boundaries. Massive mainframe server blocks in charcoal with telemetry meters "
        "and strict algorithmic governor valves preventing unbounded token loops and database exhaustion. Fine cyan engineering callouts."
    ),
    "death-of-tier-1-erp-helpdesk": (
        f"{STYLE_BASE} Minimalist editorial scene of a dark, silent enterprise operations room. Empty technical desks with single glowing monochrome terminals "
        "running automated root-cause resolution scripts, zero ticket backlogs, quiet operational efficiency in dark obsidian and slate."
    ),
    "five-day-architecture-sprint": (
        f"{STYLE_BASE} Architectural contrast artwork. A dense, perfectly compiled block of executable system architecture and code contracts in pure cyan "
        "standing monolithic against a scattered pile of generic corporate management consultant slide decks on an obsidian floor."
    ),
    "how-to-build-an-enterprise-ontology-from-scratch": (
        f"{STYLE_BASE} Comprehensive 7-layer engineering blueprint. An exploded isometric technical diagram of an enterprise domain ontology: "
        "Scoping, Invariants, Finite State Machines, FastMCP tool contracts, CDC Kafka pipeline, adversarial fuzzing, and autonomous agent orchestration."
    ),
    "how-to-build-operational-ontology-python-mcp": (
        f"{STYLE_BASE} Clean software engineering architecture diagram. Python Pydantic class models with strict type annotations connecting seamlessly "
        "to Model Context Protocol (MCP) tool endpoints. Monospace typography cues, sharp 90-degree buses, deep dark terminal canvas."
    ),
    "integration-drift": (
        f"{STYLE_BASE} Technical phase-shift diagnostic schematic. Two synchronized high-frequency event streams diverging over time, causing an "
        "immediate deterministic circuit breaker to trip in sharp cyan and alert boundary. Illustrating API schema drift prevention."
    ),
    "kafka-metamorfose-ia-futuro-do-trabalho": (
        f"{STYLE_BASE} Editorial conceptual art blending Franz Kafka's Metamorphosis with autonomous work. A stylized, geometric origami beetle crafted from "
        "dark folded slate paper, resting on a stark wooden writing desk alongside an austere modern terminal. Deep philosophical sobriety."
    ),
    "latam-airlines-case-study": (
        f"{STYLE_BASE} Aviation operational engineering schematic. An isometric technical network map of commercial flight routes, aircraft turnarounds, "
        "and gate allocations. Precision dispatch nodes calculating 3% margin optimization in crisp cyan vectors on dark obsidian."
    ),
    "legacy-core-backing-engine": (
        f"{STYLE_BASE} Heavy industrial engineering metaphor. A monolithic, impenetrable dark steel vault core representing legacy banking mainframes (SAP/COBOL), "
        "fitted with high-speed precision modular cyan optical couplers and event buses powering modern autonomous agents."
    ),
    "llm-as-judge-fallacy": (
        f"{STYLE_BASE} Conceptual technical critique. An optical chamber with two facing mirrors creating an infinite, degrading hall of mirrors (evaluator bias), "
        "cut across by an absolute, rigid steel caliper representing deterministic statutory invariant verification."
    ),
    "manifesto": (
        f"{STYLE_BASE} Minimalist architectural editorial visual. A single solid foundation stone in obsidian with fine cyan laser-etched motto, "
        "representing unyielding engineering truth against corporate marketing hype. Tactile, monolithic, grounded."
    ),
    "ontology-vs-database-schema": (
        f"{STYLE_BASE} Comparative technical schematic. Bottom layer: 2D flat database tables and foreign keys in muted grey. Top layer: an active kinetic "
        "harness of business invariants, state transition graphs, and execution perimeters in bright cyan governing the underlying data."
    ),
    "ontology-vs-knowledge-graph": (
        f"{STYLE_BASE} Dual-stack neuro-symbolic architecture diagram. A network graph of entity nodes and relationships (Knowledge Graph) strictly bounded "
        "and encapsulated by an overarching rigid rectangular frame of validation rules, mathematical invariants, and state machines (Ontology)."
    ),
    "palantir-aip-bootcamp-operational-ontology": (
        f"{STYLE_BASE} Enterprise defense-grade decision platform architecture. Multi-tier data orchestration harness connecting transactional ERP records "
        "to an executable operational ontology with kinetic action toolkits and secure MCP sandboxes."
    ),
    "palantir-pricing-tco-and-open-alternatives": (
        f"{STYLE_BASE} Conceptual economic architecture. A colossal proprietary concrete monolith gate representing proprietary vendor pricing, "
        "contrasted with a modular, lightweight, high-performance open-source architecture gateway built with cyan precision trusses."
    ),
    "palantir-vs-databricks-agent-architecture": (
        f"{STYLE_BASE} Technical architectural comparison. Left side: a deep, passive reservoir of data lake tables (static analytics). Right side: an "
        "active, kinetic operational ontology engine executing stateful atomic actions in real time via cyan event buses."
    ),
    "perimeter-isolation-mcp-data-contracts": (
        f"{STYLE_BASE} Cybersecurity and architecture blueprint. A multi-layered perimeter defense vault around core enterprise databases. "
        "Model Context Protocol (MCP) data contract checkpoints inspecting and validating payload packets through cryptographic gates in cyan."
    ),
    "protocol-arbitrage-claims-underwriting": (
        f"{STYLE_BASE} High-speed insurance underwriting schematic. Multimodal claims dossiers (telematics, medical records, photos) passing through an "
        "orthogonal scanning plane that resolves complex policy adjudications in milliseconds with pure mathematical consistency."
    ),
    "the-operational-ontology": (
        f"{STYLE_BASE} Flagship architecture blueprint of the Operational Ontology. The central kinetic engine connecting enterprise ERP/CRM via CDC streaming "
        "to deterministic invariants and atomic Model Context Protocol action registries for autonomous agents."
    ),
    "the-poc-graveyard": (
        f"{STYLE_BASE} Atmospheric editorial artwork. An expansive dark brutalist chamber of dormant enterprise servers resting on charcoal stone, "
        "with a single sharp cyan beam illuminating a live production pipeline emerging through a monolithic concrete opening."
    ),
    "unconstrained-agents-finite-state-machines": (
        f"{STYLE_BASE} Incident post-mortem schematic. A chaotic recursive loop of 42 uncontrolled API calls violently halted and contained by a rigid, "
        "orthogonal Finite State Machine (FSM) boundary box with deterministic transitions in sharp cyan #52B4FD."
    ),
    "what-is-an-ontology-for-ai-agents": (
        f"{STYLE_BASE} The definitive 5-layer hierarchy diagram of enterprise AI data. Ascending from raw SQL tables (Layer 1) up to the executable "
        "Operational Ontology (Layer 5) with invariant gatekeepers and autonomous action protocols in crisp cyan typography."
    ),
    "why-rag-breaks-on-erp": (
        f"{STYLE_BASE} Technical breakdown schematic. High-dimensional vector embeddings shattering against a double-entry general ledger balance sheet. "
        "Contrasting fuzzy cosine similarity failure with strict deterministic decimal balance assertions."
    ),
    "buy-versus-build-b2b-enterprise-crm": (
        f"{STYLE_BASE} Architectural decision matrix. Monolithic proprietary CRM seat allocation compared with a headless open-source engine, "
        "event streaming gateway, and autonomous agent dispatch system in clean 90-degree cyan blueprint blocks."
    ),
}

def main():
    base_dir = Path("/Users/hugosoares/blog_hsn_labs")
    covers_dir = base_dir / "docs/assets/images/posts"
    scratch_dir = Path("/Users/hugosoares/.hermes/cache/scratch")
    
    print(f"Total prompt specs: {len(PROMPTS)}")
    
    # Copy already validated test images
    crm_test = scratch_dir / "test_gen.png"
    poc_test = scratch_dir / "test_illustrative.png"
    
    out_crm_dir = covers_dir / "buy-versus-build-b2b-enterprise-crm"
    out_crm_dir.mkdir(parents=True, exist_ok=True)
    if crm_test.exists():
        out_crm_dir.joinpath("cover.png").write_bytes(crm_test.read_bytes())
        print("Copied test_gen.png to buy-versus-build-b2b-enterprise-crm/cover.png")
        
    out_poc_dir = covers_dir / "the-poc-graveyard"
    out_poc_dir.mkdir(parents=True, exist_ok=True)
    if poc_test.exists():
        out_poc_dir.joinpath("cover.png").write_bytes(poc_test.read_bytes())
        print("Copied test_illustrative.png to the-poc-graveyard/cover.png")
        
    # Check existing diagrams to link
    existing_assets = {
        "the-operational-ontology": base_dir / "docs/assets/diagrams/hsn-agent-architecture.png",
        "palantir-aip-bootcamp-operational-ontology": base_dir / "docs/assets/diagrams/palantir-aip-architecture-pt.png",
        "kafka-metamorfose-ia-futuro-do-trabalho": base_dir / "docs/assets/images/posts/kafka/capa-metamorfose.jpg",
        "manifesto": base_dir / "docs/assets/images/posts/manifesto/hugo-nascimento-manifesto-mesa.jpg",
        "balance-sheet-guard-bpo-extinction": base_dir / "docs/assets/images/posts/bpo/hugo-nascimento-consultoria-laptop.jpg"
    }

    # Generate each missing cover
    for slug, prompt in PROMPTS.items():
        slug_dir = covers_dir / slug
        slug_dir.mkdir(parents=True, exist_ok=True)
        target_img = slug_dir / "cover.png"
        
        if target_img.exists() and target_img.stat().st_size > 10000:
            print(f"[-] Already exists: {slug}")
            continue
            
        print(f"[+] Generating: {slug} ...")
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model='gemini-3.1-flash-image',
                    contents=[prompt],
                )
                img_bytes = None
                for part in response.parts:
                    if part.inline_data:
                        data = part.inline_data.data
                        img_bytes = data if isinstance(data, bytes) else base64.b64decode(data)
                        break
                if img_bytes:
                    target_img.write_bytes(img_bytes)
                    print(f"    Saved: {target_img} ({len(img_bytes)} bytes)")
                    time.sleep(2)  # respectful rate spacing
                    break
                else:
                    print(f"    Warning: No inline_data in response for {slug}")
            except Exception as e:
                print(f"    Attempt {attempt+1} failed: {e}")
                time.sleep(5 * (attempt + 1))

if __name__ == "__main__":
    main()
