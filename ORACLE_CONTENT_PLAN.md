# Oracle Content Engine Implementation Plan

## Purpose and Positioning
Transform primary consulting lessons and technical post-mortems into proprietary executive essays.
Target level 3 economic buyers: CFOs, CEOs, Heads of Architecture.
Voice: Caveman style, direct, authoritative, zero fluff.
Core message: Deterministic agentic engineering versus fragile probabilistic wrappers.

## 9 Target Essays

### 1. Why Traditional RAG Breaks on Enterprise ERP
- Slug: why-rag-breaks-on-erp
- Target File: docs/writing/why-rag-breaks-on-erp.md
- Core Argument: Semantic vector search cannot understand relational integrity, balance rules, or foreign keys. Cosine distance fails on financial ledgers.
- Solution: Graph-grounded business ontologies before retrieval. Immutable schema validation.

### 2. The PoC Graveyard: Why Enterprise AI Pilots Never Reach Production
- Slug: the-poc-graveyard
- Target File: docs/writing/the-poc-graveyard.md
- Core Argument: Ninety percent of generative AI prototypes collapse when exposed to messy enterprise data, security perimeters, and latency limits.
- Solution: Moving from prompt tweaking to systems engineering with automated regression test suites.

### 3. The Fallacy of LLM as a Judge in Regulated Enterprise Workflows
- Slug: llm-as-judge-fallacy
- Target File: docs/writing/llm-as-judge-fallacy.md
- Core Argument: Using probabilistic models to evaluate probabilistic outputs creates circular confirmation bias that fails external regulatory audits.
- Solution: Deterministic rule-based assertion suites, deterministic state machines, golden verification datasets.

### 4. Legacy Core Systems Will Not Die: They Are the Engine Behind Autonomous Agents
- Slug: legacy-core-backing-engine
- Target File: docs/writing/legacy-core-backing-engine.md
- Core Argument: Replacing core ERP or mainframes takes a decade and burns massive capital. Legacy code stores decades of valuable business rules.
- Solution: Reverse-engineering stored procedures and ABAP into executable ontologies. Agents act as autonomous execution layers without altering core databases.

### 5. The Structural Hazard of Unconstrained Agents: Enforcing Finite State Machines
- Slug: unconstrained-agents-finite-state-machines
- Target File: docs/writing/unconstrained-agents-finite-state-machines.md
- Core Argument: Probabilistic planning loops inevitably trigger illegal operations, balance corruptions, and severe corporate liabilities.
- Solution: Constrained execution via formal automata theory. Agents propose actions, deterministic transition guards validate preconditions, state updates atomically.

### 6. Perimeter Isolation: Safely Deploying Agents via MCP Data Contracts
- Slug: perimeter-isolation-mcp-data-contracts
- Target File: docs/writing/perimeter-isolation-mcp-data-contracts.md
- Core Argument: CISOs block agent rollouts because broad database credentials risk intellectual property leaks and privacy violations.
- Solution: Least-privilege Model Context Protocol endpoints, isolated read replicas, schema-enforced input and output contracts.

### 7. The Five-Day Architecture Sprint: De-risking Enterprise Agentic Deployment
- Slug: five-day-architecture-sprint
- Target File: docs/writing/five-day-architecture-sprint.md
- Core Argument: Management consulting slide decks engineer nothing. C-levels need empirical proof on real company systems before allocating capital.
- Solution: Forward Deployed Engineering sprint: sandbox deployment, adversarial stress testing, audited ROI case, full fee credit upon production contract.

### 8. The Collapse of Legacy RPA: Why Fragile Screen Scrapers Cannot Survive the Agentic Shift
- Slug: collapse-of-legacy-rpa
- Target File: docs/writing/collapse-of-legacy-rpa.md
- Core Argument: Traditional RPA vendors built empires selling glorified screen recorders that break on minor DOM and UI updates, extracting millions in maintenance consulting.
- Solution: Headless deterministic agents operating directly on semantic protocols and APIs, driving maintenance overhead to zero.

### 9. The C-Suite Transition Playbook: Protecting Margins in the Agentic Economy
- Slug: c-suite-margin-protection-playbook
- Target File: docs/writing/c-suite-margin-protection-playbook.md
- Core Argument: Autonomous workforces reduce unit transaction costs by ninety percent. Companies relying on legacy headcount billing or manual BPO face rapid margin erosion.
- Solution: The operational strangler pattern: routing high-friction tasks to deterministic agents while redeploying human capital to strategic supervision.

## Production and Human Navigation Architecture

### Human Navigation Quality Gates
1. MkDocs Material Navigation Structure:
   - Topic grouping in mkdocs.yml under Writing.
   - Next and Previous navigation links active on all posts.
   - Sticky table of contents on desktop right rail.
   - Filterable tags for rapid categorization: Architecture, Security, Strategy, BPO, Governance.
2. Cross-Linking and Conversion Traps:
   - Every post links to at least two related essays.
   - Every post ends with an author signature and a direct path to the 5-day Bootcamp or Advisory.
3. Visual and Mechanical Validation:
   - Build validation with mkdocs build --strict to guarantee zero 404 links.
   - Mobile drawer and responsive layout inspection via browser tools.
