---
title: Why I Never Use Normal RAG on Financial ERPs
date: '2026-08-07'
category: Deterministic Architecture & Systems
tags:
- architecture
- rag
- erp
description: "Why vector similarity retrieval corrupts arithmetic precision and ledger integrity in enterprise financial ERPs."
author: Hugo Nascimento
---

*Reading time: 4 minutes. Author: Hugo Nascimento.*

<!-- more -->

*Context: This essay came out of an emergency technical audit where an agency tried to calculate corporate accounts payable using cosine similarity over embedded invoice chunks. The resulting hallucinations almost corrupted the client ledger.*

Connecting standard Retrieval-Augmented Generation to an Enterprise Resource Planning system is an architectural trap.

Over the past two years, I have lost count of how many enterprise teams have approached me after burning months trying to make vector search read corporate financials. The premise sounds tempting to a non-technical executive: dump all purchase orders, vendor invoices, contracts, and database exports into a vector database, then let an LLM retrieve relevant chunks to answer operational questions.

In production, this approach collapses on basic arithmetic.

## Semantic Closeness Is Not Mathematical Truth

Vector embeddings measure semantic similarity in natural language. They know that words like invoice, billing, and payment share conceptual proximity.

An Enterprise Resource Planning database like SAP S/4HANA or Totvs Protheus does not care about semantic vibes. It operates on immutable double-entry bookkeeping, strict foreign key constraints, primary keys, and statutory fiscal periods.

Cosine distance is mathematically incapable of answering relational enterprise queries.

### 1. Vector Search Cannot Join Tables
Imagine a CFO asking: Which open purchase orders above fifty thousand dollars from last month lack a corresponding delivery receipt?

To answer that question correctly, an engineer must execute relational joins across at least four normalized tables: purchase orders, line items, goods receipts, and vendor tax records. 

A vector database searches for text chunks that mention purchase orders and large amounts. It cannot join foreign keys. It cannot filter out canceled records. It pulls five text snippets that sound relevant, feeds them into the prompt, and the model fabricates a plausible list that omits critical transactions.

### 2. Debits and Credits Must Zero Out
In corporate accounting, balances are absolute invariants. Every debit must match an equal credit. 

When you chunk a ledger table into vector embeddings, you slice relational rows into disconnected text fragments. The model retrieves seven out of ten line items because three fragments had lower semantic relevance scores. When the model attempts to calculate the balance, it hallucinates a sum based on incomplete data.

In enterprise finance, being ninety-five percent accurate is identical to being completely broken.

### 3. The Nightmare of Temporal Boundaries
Enterprise data is strictly bound by fiscal calendars, currency exchange rates, and tax jurisdictions. 

Vector search has no inherent concept of temporal sequence. Unless an engineer manually partitions indices by fiscal month, a semantic query will happily retrieve tax withholding rules from two years ago alongside current invoices, generating calculations that breach local tax authority requirements like SPED in Brazil or statutory reporting in North America.

## What I Build Instead: Executable Ontologies

At HSN Labs, we do not let language models guess relational SQL or search raw embeddings for financial truth. Here is the exact architecture I enforce instead:

* Pre-Compiled Business Ontologies: We map the enterprise schema into an explicit knowledge graph that defines verified relationships, valid join paths, and business rules before any query runs.
* Strictly Typed Query Generation: The agent does not generate open-ended SQL strings. It selects parameterized query templates validated against strict Pydantic schemas. Every parameter is checked before it touches the read replica.
* Hard Invariant Assertions: When the database returns records, code-level assertion layers verify ledger balances, currency alignment, and temporal validity before context reaches the user or downstream worker.

If an architecture cannot guarantee mathematical precision on financial records, it does not belong in enterprise production.

## Strategic Resources and Related Essays
- <a href="../the-poc-graveyard/">Why Agents Fail: The PoC Graveyard</a>
- <a href="../cost-legacy-it/">The Cost of Unbounded AI in Legacy IT</a>
- <a href="https://hsnlabs.ai/bootcamp">Apply for the HSN Labs Five-Day Architecture Bootcamp</a>
