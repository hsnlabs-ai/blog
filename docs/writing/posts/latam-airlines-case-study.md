---
date: 2026-09-13
authors:
  - hugo
categories:
  - Engineering
  - Case Study
tags:
  - ROI
  - Agentic-Engineering
---

# LATAM Airlines: Deterministic Agents in a 3% Margin Business

Airlines run on 3% margins. 31% of their operating cost is jet fuel. There is no slack.

If an AI agent does not create immediate value or cut costs, it dies.

I analyzed LATAM Airlines' deployment of customer experience agents in production. They process millions of interactions. They learned three hard lessons about agentic engineering at scale.

## 1. Semantic Decentralization Burns Money
LATAM initially built specialist agents (flights, hotels, insurance). Each agent reasoned and generated final structured outputs.

Result: 15% overhead in token consumption and latency.

Fix: Strict Supervisor pattern. Specialist agents became blind tool executors. The Supervisor node handles all final semantic formatting.

**Takeaway:** Do not ask every node in your graph to reason about output structure. Centralize formatting. Cut costs by 15% without losing quality.

## 2. Telemetry Beats Prompt Hacking
In production, 13% of user interactions failed routing. The system flagged them as "out of scope."

Amateurs add prompt penalties to stop hallucinations. LATAM looked at LangSmith telemetry.

Data showed 95% of those failed queries were legitimate passenger needs (baggage, check-in). The model didn't fail. The architecture didn't fail. The business logic was simply incomplete.

Fix: Added a dedicated Customer Care node. Routing errors dropped to 1%.

**Takeaway:** Observe production telemetry. Build deterministic nodes for reality, not for your happy path.

## 3. The Chatbot Is Not The Product
This is my core thesis. 

A B2C chatbot is just a data collection interface. Conversations are cheap. Structured signals are valuable.

LATAM realized this. They built Compass: an internal engine that takes unstructured chat logs, applies strict semantic ontologies, and outputs a Knowledge Graph directly into BigQuery. 

When a passenger asks about "Italian restaurants near the hotel," they aren't just chatting. They are feeding a deterministic pipeline with semantic preferences.

Stop building free-text wrappers. Use AI as a ruthless parser to turn noise into structured production data. 

That is how you replace legacy IT. That is how you expand margins. That is how you prove ROI to a CFO.