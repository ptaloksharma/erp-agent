# erp-agent — Business Context

> Read this file before writing any agent logic. It is the single source of
> truth for *why* this agent exists and *what* it must do.

## 1. Mission
**Use-case:** Routes enterprise ERP user requests securely down the mesh and delegates domain tasks to specialized agents.

## 2. Business Requirements
```
Enterprise ERP UI Coordinator Agent (erp-agent). Core Responsibilities & Constraints: 1. Intent Classification: Receive raw natural language requests from enterprise users or web hooks, and classify intents accurately (e.g., AP invoice processing, procurement, ledger status). 2. Mesh Routing & Delegation: Securely delegate domain-specific tasks down the hierarchical mesh to registered domain agents (such as ap-invoice-agent) using cryptographically signed HMAC audit receipts and verified goalHash integrity. 3. Security & Governance: Enforce BOLA tenant isolation, strict scope validation, and policy checks via DshSecurityBridge before any inter-agent handoff occurs. 4. UI & Observability: Expose standardized JSON/SSE telemetry outputs for integration with the Buddy control plane dashboard and render local architecture states.
```

## 3. Guardrail Contract
| Setting | Value |
|---|---|
| Strictness | `standard` |
| Compliance packs | `bola, gdpr` |
| Telemetry | `stdout` |
| Cloud target | `azure` |

These are *enforced by the Securi bridge* — they are not suggestions. Every
tool this agent exposes is wrapped with BOLA/RBAC/loop-guard interception.

## 4. Domain Rules (fill in as the business specifies)
- _Business rule 1 …_
- _Business rule 2 …_

## 5. Non-Goals
- _What this agent must NOT do (helps prevent scope creep / hallucinated features)_

## 6. Success Criteria
- _How the business will know this agent works (measurable outcomes)_
