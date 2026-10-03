import os
import sys
import time
import json
import base64
from pathlib import Path
from PIL import Image
from google import genai

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
    "A high-end editorial conceptual photograph for HSN Labs, perfectly matching the visual brand aesthetic of https://hsnlabs.ai/. "
    "Tactile physical white origami paper sculptures with crisp geometric folds and visible paper fiber texture, "
    "contrasted with clean geometric architectural elements and the iconic pure vibrant sky blue (#52B4FD) acrylic or water square. "
    "Clean, pristine studio lighting, soft natural contact shadows, neutral off-white to subtle gradient background. "
    "Strictly zero text, no words, no letters, no numbers, no typography, no language. 16:9 aspect ratio."
)

PROMPTS = {
    "how-to-build-an-enterprise-ontology-from-scratch": (
        f"{STYLE_BASE} Subject: 7-Phase Architecture. A majestic 7-tier stepped architectural origami pyramid sculpture crafted from crisp folded white cardstock. "
        "Each ascending tier exhibits sharp 90-degree creases and interlocking folds, resting firmly on a solid vibrant sky blue (#52B4FD) square plinth."
    ),
    "the-operational-ontology": (
        f"{STYLE_BASE} Subject: The Kinetic Operational Engine. An intricate, pristine white origami kinetic mechanism with interlocking geometric facets "
        "and razor-sharp paper folds, anchored securely upon the official vibrant sky blue (#52B4FD) acrylic water square pedestal."
    ),
    "how-to-build-operational-ontology-python-mcp": (
        f"{STYLE_BASE} Subject: Code and Contracts. Two modular geometric origami paper blocks fitting together with microscopic mechanical precision, "
        "locked in place by a single vibrant sky blue (#52B4FD) acrylic key insert."
    ),
    "chatbot-vs-agent": (
        f"{STYLE_BASE} Subject: Chatbot vs Agent. On the left, a delicate, crumpled, fragile ball of thin paper. "
        "On the right, a monolithic, perfectly folded crisp white origami architectural obelisk with sharp 90-degree creases, "
        "resting firmly atop a solid vibrant sky blue (#52B4FD) acrylic square pedestal."
    ),
    "cleveland-clinic-case-study-operational-agents": (
        f"{STYLE_BASE} Subject: Healthcare Bed Flow. An architectural modular origami pavilion of interconnected white paper rooms and corridors, "
        "with subtle translucent sky blue and emerald green geometric facets indicating verified capacity."
    ),
    "latam-airlines-case-study": (
        f"{STYLE_BASE} Subject: Aviation Precision. A sleek, highly aerodynamic white origami aircraft sculpture taking flight dynamically above a "
        "clean grid-scored paper runway surface on a sky blue (#52B4FD) acrylic base."
    ),
    "legacy-core-backing-engine": (
        f"{STYLE_BASE} Subject: Heavy Industrial Core. A massive, impenetrable monolithic dark steel vault block resting on the floor, "
        "seamlessly fitted with modern precision white origami wings and high-speed sky blue (#52B4FD) glass couplers."
    ),
    "perimeter-isolation-mcp-data-contracts": (
        f"{STYLE_BASE} Subject: Perimeter Defense. Concentric geometric rings of sharp white folded origami walls forming a secure citadel, "
        "protecting a glowing sky blue (#52B4FD) cubic core in the center."
    ),
    "unconstrained-agents-finite-state-machines": (
        f"{STYLE_BASE} Subject: Taming Infinite Loops. A wild, spiraling white paper ribbon coiling erratically, "
        "abruptly caught, straightened, and contained inside a rigid rectangular origami boundary box on a sky blue (#52B4FD) plinth."
    ),
    "ontology-vs-knowledge-graph": (
        f"{STYLE_BASE} Subject: Network bounded by Invariants. An intricate network web of delicate white folded paper strands (knowledge graph), "
        "encapsulated and held taut within a heavy rigid square frame of solid sky blue (#52B4FD) acrylic (ontology rules)."
    ),
    "palantir-aip-bootcamp-operational-ontology": (
        f"{STYLE_BASE} Subject: Enterprise Decision Platform. A complex, multi-faceted geometric origami polyhedron with diamond-cut paper facets, "
        "cradled securely in an architectural sky blue (#52B4FD) precision stand."
    ),
    "five-day-architecture-sprint": (
        f"{STYLE_BASE} Subject: Speed and Architecture. A solid, monolithic 5-stepped origami tower in pristine white paper, each tier folded in rapid succession, "
        "standing tall over scattered flat unfolded paper sheets."
    ),
    "autonomous-negotiations-collections-contracts": (
        f"{STYLE_BASE} Subject: Autonomous Negotiation. Two elegant, stylized white origami paper cranes meeting beak-to-beak in perfect harmony across a "
        "vibrant sky blue (#52B4FD) square bridge on a minimalist surface."
    ),
    "balance-sheet-guard-bpo-extinction": (
        f"{STYLE_BASE} Subject: Balance Sheet Guard. A minimal balance scale: on one tray a heavy, rough dark charcoal block; "
        "on the other tray, a featherlight, razor-sharp white origami geometric prism on a sky blue (#52B4FD) block tipping the scale with ease."
    ),
    "bpo-replacement-matrix": (
        f"{STYLE_BASE} Subject: Replacement Matrix. A neat, stepped matrix grid of white origami cubes arranged in precise ascending rows "
        "across a monolithic sky blue (#52B4FD) acrylic platform."
    ),
    "buy-versus-build-b2b-enterprise-crm": (
        f"{STYLE_BASE} Subject: Buy vs Build. A heavy, monolithic closed iron cube on one side, contrasted with light, modular, "
        "interlocking white origami geometric blocks on the other side, connected by sky blue (#52B4FD) joints."
    ),
    "c-suite-margin-protection-playbook": (
        f"{STYLE_BASE} Subject: Margin Defense. An elegant, layered white origami geometric shield sculpture, protecting a pure sky blue (#52B4FD) "
        "cubic core from external pressure."
    ),
    "collapse-of-legacy-rpa": (
        f"{STYLE_BASE} Subject: Fragile Screen Automation. A mechanical gear folded out of thin paper tearing and collapsing under torque, "
        "while an unyielding, sleek white origami prism passes cleanly through it."
    ),
    "cost-legacy-it": (
        f"{STYLE_BASE} Subject: Cost Containment. A massive dark slate block firmly encircled and held in check by crisp white origami geometric bands "
        "locked with a sky blue (#52B4FD) acrylic clasp."
    ),
    "death-of-tier-1-erp-helpdesk": (
        f"{STYLE_BASE} Subject: Silent Operations. A tranquil, sculptural minimalist scene with a tiny folded white origami desk and chair, completely clean, "
        "with a single glowing sky blue (#52B4FD) square resting in quiet perfection."
    ),
    "kafka-metamorfose-ia-futuro-do-trabalho": (
        f"{STYLE_BASE} Subject: Kafka Metamorphosis. An intricate, beautifully folded white origami beetle sculpture resting alongside a "
        "pure sky blue (#52B4FD) square block on a minimalist paper canvas."
    ),
    "manifesto": (
        f"{STYLE_BASE} Subject: The HSN Labs Manifesto. A single, magnificent white origami carp leaping with dynamic kinetic grace directly out of "
        "a vibrant sky blue (#52B4FD) acrylic water cube, soaring upward."
    ),
    "palantir-pricing-tco-and-open-alternatives": (
        f"{STYLE_BASE} Subject: Vendor Lock-in Barrier. A towering, closed dark concrete wall contrasted with an inviting, "
        "modular open archway crafted from sharp white origami struts and sky blue (#52B4FD) pillars."
    ),
    "protocol-arbitrage-claims-underwriting": (
        f"{STYLE_BASE} Subject: Protocol Arbitrage. Multiple delicate folded white paper leaves passing through a sharp vertical sky blue (#52B4FD) "
        "optical acrylic slit, consolidating instantly into a single solid crystalline prism."
    ),
    "the-poc-graveyard": (
        f"{STYLE_BASE} Subject: The PoC Graveyard. Miniature folded white origami paper airplanes resting quietly on the ground in the foreground, "
        "while in the background a majestic white origami carp leaps high out of a sky blue (#52B4FD) water cube."
    ),
    "why-rag-breaks-on-erp": (
        f"{STYLE_BASE} Subject: RAG vs ERP. A porous, delicate white origami paper lattice colliding and buckling against a monolithic, "
        "unyielding dark slate cube, anchored on a sky blue (#52B4FD) pedestal."
    ),
    "integration-drift": (
        f"{STYLE_BASE} Subject: Schema Drift. Two parallel white origami folding tracks that suddenly branch apart, with the divergent track "
        "immediately blocked by a strict sky blue (#52B4FD) acrylic gate."
    ),
    "llm-as-judge-fallacy": (
        f"{STYLE_BASE} Subject: LLM-as-a-Judge Fallacy. Two identical white origami bird sculptures facing each other in an infinite hall of reflections, "
        "interrupted cleanly by a solid sky blue (#52B4FD) caliper beam."
    ),
    "ontology-vs-database-schema": (
        f"{STYLE_BASE} Subject: Beyond Flat Schemas. A flat 2D sheet of paper with simple grid creases on the surface, supporting an intricate, "
        "three-dimensional white origami architectural structure rising into the air on a sky blue (#52B4FD) base."
    ),
    "palantir-vs-databricks-agent-architecture": (
        f"{STYLE_BASE} Subject: Lake vs Kinetic Engine. A shallow, still rectangular basin of dark calm water on one side, paired with an "
        "active kinetic white origami turbine wheel mounted on a sky blue (#52B4FD) motor block."
    ),
    "what-is-an-ontology-for-ai-agents": (
        f"{STYLE_BASE} Subject: Five Layers of Data. An elegant 5-step ascending staircase of folded white cardstock, rising from a flat unfolded sheet "
        "at the bottom to a crowned geometric origami sculpture atop a sky blue (#52B4FD) platform."
    ),
}

def process_image(src_path, webp_out):
    with Image.open(src_path) as im:
        im = im.convert('RGB')
        target_w, target_h = 1200, 675
        w, h = im.size
        target_aspect = target_w / target_h
        current_aspect = w / h
        if current_aspect > target_aspect:
            new_w = int(h * target_aspect)
            offset = (w - new_w) // 2
            im = im.crop((offset, 0, offset + new_w, h))
        elif current_aspect < target_aspect:
            new_h = int(w / target_aspect)
            offset = (h - new_h) // 2
            im = im.crop((0, offset, w, offset + new_h))
        im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        im.save(webp_out, 'WEBP', quality=88, method=6)

def main():
    base_dir = Path("/Users/hugosoares/blog_hsn_labs")
    covers_dir = base_dir / "docs/assets/images/posts"
    scratch_dir = Path("/Users/hugosoares/.hermes/cache/scratch")
    
    # Pre-copy test images
    tests = {
        "chatbot-vs-agent": scratch_dir / "test_symbolic_chatbot.png",
        "the-poc-graveyard": scratch_dir / "test_symbolic_graveyard.png",
        "why-rag-breaks-on-erp": scratch_dir / "test_symbolic_rag.png"
    }
    for slug, test_file in tests.items():
        if test_file.exists():
            slug_dir = covers_dir / slug
            slug_dir.mkdir(parents=True, exist_ok=True)
            raw_png = slug_dir / "cover_symbolic.png"
            raw_png.write_bytes(test_file.read_bytes())
            process_image(raw_png, slug_dir / "cover.webp")
            print(f"[+] Reused test image for {slug}")

    print(f"Total prompt specs: {len(PROMPTS)}")
    
    for slug, prompt in PROMPTS.items():
        slug_dir = covers_dir / slug
        slug_dir.mkdir(parents=True, exist_ok=True)
        raw_png = slug_dir / "cover_symbolic.png"
        webp_out = slug_dir / "cover.webp"
        
        if raw_png.exists() and raw_png.stat().st_size > 10000 and webp_out.exists():
            print(f"[-] Already done: {slug}")
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
                    raw_png.write_bytes(img_bytes)
                    process_image(raw_png, webp_out)
                    print(f"    Saved: {webp_out} ({webp_out.stat().st_size} bytes)")
                    time.sleep(2)
                    break
                else:
                    print(f"    Warning: No inline_data for {slug}")
            except Exception as e:
                print(f"    Attempt {attempt+1} failed: {e}")
                time.sleep(5 * (attempt + 1))

if __name__ == "__main__":
    main()
