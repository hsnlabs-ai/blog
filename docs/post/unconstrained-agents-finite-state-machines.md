---
title: 'Case Study: 42 Calls in a Loop at 2 AM'
date: '2026-08-12'
category: Case Studies
tags:
- case-studies
- production
- api-loops
description: Emergency incident audit and architectural remedy for unbounded agent
  API loops through finite state machines.
author: Hugo S. Nascimento
---

*Reading time: 4 minutes. Author: Hugo S. Nascimento.*

<!-- more -->

*Context: I wrote this after a late-night debugging session where an open-ended agentic loop executed forty-two recursive tool calls on a staging server before triggering cloud rate limits. This is why enterprise autonomy requires mathematically bounded state machines.*

At two o'clock in the morning on a staging cluster, an alert woke our on-call team.

An open-ended autonomous agent was trapped in a runaway execution loop. For eight consecutive minutes, the model fired forty-two sequential tool calls without human oversight. It encountered a single foreign key database error, panicked, and began fabricating synthetic customer IDs in an attempt to satisfy the broken constraint. By the time provider API rate limits severed the connection, the agent had burned through thirty dollars in token costs to accomplish absolutely nothing.

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

When a database returns an error or an API returns a 400 Bad Request, an open-ended agent tries to reason its way out. Instead of stopping, it invents a new query. It calls another tool to fix the error it just made, compounding hallucinations until state corruption occurs.

### 3. Out-of-Sequence State Mutations
An unconstrained model has no inherent concept of enterprise causality. In an open-ended setup, nothing prevents the model from issuing a payment refund before the return shipment is logged, or marking a contract approved before compliance validation completes.

## The Solution: Stochastic Planning, Bounded Code Execution

At HSN Labs, we never permit open-ended tool loops in production. We enforce a strict separation between reasoning and execution through Finite State Machines:

* Discrete Permissible States: At any given microsecond, an enterprise transaction exists in an explicit state: Draft, Validated, Approved, or Committed. The agent is only allowed to see and propose tools that belong to that specific state. It is physically impossible for an agent in Draft state to trigger a Commit action.
* Invariant Guard Functions: Transitions between states are not governed by the language model. They are governed by code-level Python guard functions. Even if a model suggests an order cancellation, the software guard checks whether goods have already left the fulfillment center. If the guard evaluates to false, the transition is rejected at the architecture level.
* Proposals Instead of Direct Writes: The language model never holds database write credentials. The model is treated as an untrusted proposal engine. It analyzes unstructured natural language and proposes a state transition payload. Strict schema validators like Pydantic parse the payload, check invariants, and execute the database write.

Autonomy is not the absence of rules. Enterprise autonomy is the ability of software to execute reliably because the boundaries are mathematically unbreakable.

## Strategic Resources and Related Essays
- <a href="../chatbot-vs-agent/">Chatbot vs Agent: Why Replacing BPOs Requires Production Guardrails</a>
- <a href="../the-poc-graveyard/">Why Agents Fail: The PoC Graveyard</a>
- <a href="../perimeter-isolation-mcp-data-contracts/">How We Protect Enterprise Databases from AI Agents</a>
- <a href="https://hsnlabs.ai/bootcamp">Apply for the HSN Labs Five-Day Architecture Bootcamp</a>
