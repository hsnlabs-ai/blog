---
date: 2026-08-12
authors:
  - hugo
categories:
  - Engineering
  - Safety
---

# The Structural Hazard of Unconstrained Agents: Enforcing Finite State Machines

*Reading time: 4 minutes. Author: Hugo Nascimento.*

*Context: I wrote this after a late-night debugging session where an open-ended agentic loop executed forty-two recursive tool calls on a staging server before triggering cloud rate limits. This is why enterprise autonomy requires mathematically bounded state machines.*

Letting a large language model execute tools inside an open-ended reasoning loop in production is an engineering disaster waiting to happen.

If you browse GitHub or watch online agent tutorials, you will find the same ubiquitous design pattern: the ReAct loop. You give the model a system prompt, pass an array of thirty different Python functions, and tell it to think step-by-step, invoke any tool it wants, inspect the output, and keep looping until it feels the task is complete.

In a YouTube tutorial with two dummy functions, this looks magical.

In an enterprise banking or ERP environment with real money and real databases, an unconstrained ReAct loop is an unmitigated liability.

## The Mathematical Collapse of Unconstrained Probability

Language models are stochastic next-token predictors. Every tool selection is a probabilistic bet. 

When you chain probabilistic bets inside an open-ended loop, the mathematics work aggressively against you:

### 1. Compounding Probability Collapse
Suppose your model has a ninety percent probability of picking the correct tool and parameters on any single step. 

If a business workflow requires five consecutive steps, the probability of the entire chain executing without error is fifty-nine percent. By step seven, you are down to forty-seven percent. You are essentially flipping a coin on whether your production system will execute or crash.

### 2. The Hallucination Repair Death Spiral
What happens when an unconstrained agent makes a mistake? 

When a database returns a foreign key error or an API returns a 400 Bad Request, an open-ended agent tries to reason its way out. Instead of stopping, it invents a new query. It calls another tool to fix the error it just made. 

At two o'clock in the morning on a staging cluster, I watched an unconstrained agent loop for eight minutes, firing forty-two sequential tool calls, creating fake customer IDs in an attempt to satisfy a broken constraint, before finally hitting provider API limits. That single runaway loop burned thirty dollars in tokens to accomplish absolutely nothing.

### 3. Out-of-Sequence State Mutations
An unconstrained model has no inherent concept of enterprise causality. In an open-ended setup, nothing prevents the model from issuing a payment refund before the return shipment is logged, or marking a contract approved before compliance validation completes.

## The Solution: Stochastic Planning, Deterministic Execution

At HSN Labs, we never permit open-ended tool loops in production. We enforce a strict separation between reasoning and execution through Finite State Machines:

* Discrete Permissible States: At any given microsecond, an enterprise transaction exists in an explicit state: Draft, Validated, Approved, or Committed. The agent is only allowed to see and propose tools that belong to that specific state. It is physically impossible for an agent in Draft state to trigger a Commit action.
* Invariant Guard Functions: Transitions between states are not governed by the language model. They are governed by deterministic Python guard functions. Even if a model suggests an order cancellation, the software guard checks whether goods have already left the fulfillment center. If the guard evaluates to false, the transition is rejected at the architecture level.
* Proposals Instead of Direct Writes: The language model never holds database write credentials. The model is treated as an untrusted proposal engine. It analyzes unstructured natural language and proposes a state transition payload. Deterministic schema validators like Pydantic parse the payload, check invariants, and execute the database write.

Autonomy is not the absence of rules. Enterprise autonomy is the ability of software to execute reliably because the boundaries are mathematically unbreakable.

## Strategic Resources and Related Essays
- <a href="../../2026/07/22/chatbot-vs-agent-why-replacing-bpos-requires-deterministic-guardrails/">Chatbot vs Agent: Why Replacing BPOs Requires Deterministic Guardrails</a>
- <a href="../../2026/09/01/the-poc-graveyard-why-enterprise-ai-pilots-never-reach-production/">The PoC Graveyard: Why Enterprise AI Pilots Never Reach Production</a>
- <a href="../perimeter-isolation-safely-deploying-agents-via-mcp-data-contracts/">Perimeter Isolation: Safely Deploying Agents via MCP Data Contracts</a>
- <a href="https://hsnlabs.ai/bootcamp">Apply for the HSN Labs Five-Day Architecture Bootcamp</a>