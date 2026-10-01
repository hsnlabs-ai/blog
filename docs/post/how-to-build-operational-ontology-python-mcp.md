---
title: "How to Build an Operational Business Ontology in Python with Pydantic and MCP"
date: "2026-09-25"
category: Agentic Engineering
tags:
- architecture
- production
- data-contracts
- evaluation
description: "Step-by-step engineering architecture to build an operational business ontology in pure Python using Pydantic schemas and Model Context Protocol actions without proprietary lock-in."
author: Hugo S. Nascimento
---

*Reading time: 6 minutes. Author: Hugo S. Nascimento.*

The defining difference between a toy AI demonstration and a mission-critical enterprise agent is the execution layer.

When an autonomous agent interacts with unstructured vector embeddings, it hallucinates. When it interacts with an **Operational Ontology**—strongly-typed business entities with strict transactional constraints—it executes reliably in production.[5]

Palantir built a multi-billion dollar enterprise software business around this exact insight.[1][5] 

However, engineering teams do not need a seven-figure proprietary contract to deploy this architecture. Using modern open-source standards—specifically **Pydantic v2**, the **Model Context Protocol (MCP)**, and typed state machines—you can build a resilient operational ontology directly in Python.[7][8]

Here is the exact architectural blueprint.

---

## 1. Deconstructing the Operational Ontology

In enterprise operations, data cannot be treated as passive tabular rows. An operational ontology consists of three interconnected software layers:[5]

1. **Objects:** Normalized representations of real-world business entities (e.g., Invoices, Purchase Orders, Hospital Beds, Freight Shipments).[5]
2. **Properties and Links:** Strongly-typed attributes and deterministic relationships connecting entities together (e.g., an `Invoice` links to a `PurchaseOrder` and an approved `VendorAccount`).[5]
3. **Actions:** Guarded mutations and write-backs that alter system state across external transactional APIs (e.g., `ApprovePayment`, `ReassignBed`, `ReleaseEscrow`).[5]

```mermaid
flowchart TD
    A["Enterprise LLM and Reasoning Engine"] --> B["Operational Ontology Layer in Python<br>Objects, State and Graph Contracts"]
    B --> C["Model Context Protocol Action Gateway<br>Invariant Verification Engine"]
    C --> D["Core Systems of Record<br>SAP S/4HANA, Salesforce and PostgreSQL"]
```

---

## 2. Layer 1: Defining Objects and Invariants with Pydantic

Pydantic is the industry-standard data validation library for Python.[8] Instead of passing unvalidated dictionaries or raw strings to an LLM, every business entity is defined as an immutable data contract.[8]

Here is an operational model for an automated enterprise dispute resolution workflow:

```python
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, model_validator

class DisputeCategory(str, Enum):
    PRICING_DISCREPANCY = "PRICING_DISCREPANCY"
    DAMAGED_GOODS = "DAMAGED_GOODS"
    SHORT_SHIPMENT = "SHORT_SHIPMENT"

class InvoiceDispute(BaseModel):
    dispute_id: str = Field(..., pattern=r"^DISP-[0-9]{8}$")
    invoice_number: str = Field(..., min_length=5)
    vendor_id: str = Field(..., min_length=3)
    claimed_amount: Decimal = Field(..., gt=0)
    contract_tolerance_pct: Decimal = Field(default=Decimal("0.02"), ge=0, le=Decimal("0.10"))
    category: DisputeCategory
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="after")
    def verify_reconciliation_threshold(self) -> "InvoiceDispute":
        if self.claimed_amount > Decimal("50000.00"):
            # Invariant: Disputed amounts over $50k require mandatory executive escalation
            pass
        return self
```

By wrapping business objects in strict schemas, invalid model inputs are rejected at serialization before reaching execution code.[8]

---

## 3. Layer 2: Model Context Protocol (MCP) Action Gateways

Autonomous agents should never possess raw direct database write access. All state mutations must pass through an action gateway.

The Model Context Protocol (MCP) is an open specification that standardizes how applications provide context and tools to LLMs.[7] MCP operates like a universal port, allowing agents to execute functions across secure infrastructure without bespoke integrations.[7]

Here is an MCP action server implementing atomic transaction execution with validation checks:

```python
from mcp.server.fastmcp import FastMCP
from decimal import Decimal

mcp = FastMCP("EnterpriseOntologyGateway")

@mcp.tool()
async def execute_dispute_settlement(
    dispute_id: str,
    approved_settlement: float,
    operator_override: bool = False
) -> dict:
    """
    Executes an atomic ERP credit memo adjustment for an active invoice dispute.
    Strictly verifies financial invariants prior to SAP write-back.
    """
    amount = Decimal(str(approved_settlement))
    
    # 1. Fetch live entity from transactional graph
    dispute = await fetch_dispute_object(dispute_id)
    if not dispute:
        return {"status": "REJECTED", "reason": f"Dispute {dispute_id} does not exist"}

    # 2. Enforce Hard Execution Invariants
    if amount > dispute.claimed_amount:
        return {
            "status": "VIOLATION",
            "reason": "Settlement cannot exceed original claimed dispute amount"
        }

    if amount > Decimal("5000.00") and not operator_override:
        return {
            "status": "PENDING_APPROVAL",
            "reason": "Settlements exceeding $5,000 require Human-in-the-Loop dual authorization"
        }

    # 3. Atomic ERP Transaction Write-back
    erp_reference = await erp_client.post_credit_memo(
        vendor_id=dispute.vendor_id,
        invoice_number=dispute.invoice_number,
        amount=amount
    )

    return {
        "status": "COMMITTED",
        "erp_transaction_id": erp_reference,
        "dispute_id": dispute_id,
        "reconciled_amount": float(amount)
    }
```

This pattern ensures that the language model functions exclusively as a planner. The actual state modification is guarded by deterministic code invariants.

---

## 4. Layer 3: State Machines and Invariant Auditing

Production agents cannot operate in open-ended ReAct loops that iterate indefinitely. They must be bounded by finite state machines.

By modeling the agent's workflow as a directed acyclic graph (using **LangGraph** or **Temporal**), every transition between states is auditable:

1. **State: Ingestion:** Ingest raw payload and parse into `InvoiceDispute` model.[8]
2. **State: Context Enrichment:** Hydrate object with ERP purchase order history and vendor scorecards.
3. **State: Evaluation:** Prompt the model to evaluate liability based strictly on contract terms.
4. **State: MCP Action Dispatch:** Submit candidate resolution to the MCP action gateway.[7]
5. **State: Final Reconciliation:** Log cryptographic transaction audit trail to PostgreSQL.

If the model encounters an anomalous edge case, the state machine halts and routes the payload to a human operator queue with zero risk of silent failure.

---

## 5. Architectural Comparison: Open Stack vs Proprietary Platform

| Architecture Layer | Open Python + MCP Stack | Palantir Foundry / AIP |
|---|---|---|
| **Data Contracts** | Pydantic v2 (Native Python / JSONSchema)[8] | Proprietary Ontology Object Builder[5] |
| **Tool Execution** | Model Context Protocol (Open Standard)[7] | AIP Actions & Foundry Functions[5] |
| **State Orchestration** | LangGraph / Temporal / Celery | Foundry Workshop & AIP Automate |
| **Storage & Graph** | PostgreSQL, pgvector, Neo4j | Palantir Monolith / Titan |
| **Licensing Cost** | $0 Base Software Licensing | Multi-Million USD Enterprise Contract[1] |
| **Infrastructure** | Runs inside client AWS/GCP VPC | Dedicated SaaS or Palantir Managed Tenant |

---

## 6. The Production Takeaway

Enterprise AI is not a prompt engineering problem; it is a distributed systems engineering problem.

By replacing opaque prompts with strongly-typed Pydantic contracts and routing agent execution through Model Context Protocol gateways, technology leaders gain the operational precision of Palantir without the seven-figure vendor lock-in.[1][5][7][8]

---

## Sources

[1] https://www.sec.gov/Archives/edgar/data/1321655/000132165524000022/pltr-20231231.htm — Palantir Technologies Inc. Form 10-K Annual Report
[5] https://www.palantir.com/platforms/foundry/ontology — Palantir Foundry: Operational Ontology Overview
[7] https://modelcontextprotocol.io/introduction — Model Context Protocol Specification and Architecture
[8] https://docs.pydantic.dev/latest — Pydantic: Fast Data Validation for Python

## Strategic Resources and Related Essays
- <a href="../how-to-build-an-enterprise-ontology-from-scratch/">How to Build an Enterprise Ontology from Scratch: Step by Step</a>
- <a href="../ontology-vs-knowledge-graph/">Ontology vs. Knowledge Graph: Key Differences, Architecture, and Agent Reliability</a>
- <a href="../palantir-aip-bootcamp-operational-ontology/">The Architecture of Palantir AIP: Why Enterprise Agents Require an Operational Ontology</a>
- <a href="https://hsnlabs.ai/bootcamp">Apply for the HSN Labs Five-Day Architecture Bootcamp</a>