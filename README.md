# HBA — Hermes Berserk Armor

A single Hermes agent, running across a small fleet, wrapped in a full set of
self-built tools. HBA is the meta-repository that assembles those tools into one
coherent system: the memory it thinks with, the tools it works and acts with,
and the controls that keep it contained.

The design principle is simple: **maximise capability, bound the blast radius.**
The agent is given real power — a real browser, real secrets, real infrastructure
access — and every one of those powers is paired with a control that limits what
an attacker could do if the agent were ever turned.

![fleet architecture](assets/fleet-architecture.png)

---

## The fleet

The same agent runs on three bodies, sharing one memory and one toolset:

| Body | Role | Backed by |
|------|------|-----------|
| Hermes · Azure | Cloud node, always reachable | Azure GPU / VM |
| Hermes · k3s | 24/7 harness cluster, GitOps | `Harness-Cluster` (Flux CD) |
| Hermes · Local | Hardware-gated workstation | this Mac, always on |

---

## Components

Public components are vendored here as git submodules under `components/`.
Private components are listed for completeness.

### Core — memory

The agent's persistent memory: what it knows, and what it remembers about you.

| Component | Status | Description |
|-----------|--------|-------------|
| [`brain-rag-server`](components/core/brain-rag-server) | public · submodule | Local hybrid-RAG MCP server over a markdown/Obsidian vault. Embeddings + BM25, merged with reciprocal rank fusion. No cloud, no GPU, no daemon. |
| `mem0 / pgvector` | integration | Long-term agent memory (facts, preferences) persisted in Postgres/pgvector, surviving restarts and shared across bodies. |
| `neuromancer-mcp` | private | Memory MCP for agents. |

### Reach — working and acting tools

What the agent uses to see, act, and stay efficient.

| Component | Status | Description |
|-----------|--------|-------------|
| [`mcp-scalpel`](components/reach/mcp-scalpel) | public · submodule | Semantic filter proxy for the Docker MCP Gateway. Routes `tools/list` to the relevant subset and cuts per-turn catalog tokens by 35–52%. Fully local. |
| `ab-live` | private | Drives your real browser — cookies, sessions, extensions — live inside the Hermes pane. Not a headless throwaway; the actual browser. |
| `excalibur` | private | Turns a raw nuclei scan into a scope-enforced, submission-ready report. |
| `Mando` | private | Autonomous bug-bounty operator (Hermes + Boba MCP + Exegol). |

### Defense — containment

Every power is paired with a control. This is what bounds the blast radius.

| Component | Status | Description |
|-----------|--------|-------------|
| [`heucat`](components/defense/heucat) | public · submodule | Serves API keys from the macOS Secure Enclave behind Touch ID instead of a plaintext `.env`. The key never leaves the enclave. |
| [`hermes-chthonios`](components/defense/hermes-chthonios) | public · submodule | Seals an agent profile at rest. The agent can encrypt but physically cannot decrypt without a YubiKey (touch + PIN) — a sealed profile cannot read a single API key. |
| [`hermes-argus`](components/defense/hermes-argus) | public · submodule | Read-only security auditor. Cross-checks config against listening ports, grades exposure honestly, never reads or writes a secret. |

### Control — visibility and steering

| Component | Status | Description |
|-----------|--------|-------------|
| `KubeShip` | private | Pilot the Kubernetes fleet through a visual interface — the infrastructure, made observable and steerable. |
| `Harness-Cluster` | private | The GitOps k3s cluster that runs the agents 24/7 (Flux CD). |

---

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full diagram and data flow.

The animated schematic is in [`assets/fleet-architecture.mp4`](assets/fleet-architecture.mp4).

---

## Working with submodules

Clone with all public components:

```bash
git clone --recurse-submodules https://github.com/iacker/HBA.git
```

If already cloned:

```bash
git submodule update --init --recursive
```

Update every component to its latest upstream commit:

```bash
git submodule update --remote --merge
```

---

## Repository layout

```
HBA/
├── README.md
├── components/
│   ├── core/
│   │   └── brain-rag-server/     (submodule)
│   ├── reach/
│   │   └── mcp-scalpel/          (submodule)
│   └── defense/
│       ├── heucat/               (submodule)
│       ├── hermes-chthonios/     (submodule)
│       └── hermes-argus/         (submodule)
├── docs/
│   └── ARCHITECTURE.md
├── prompts/
│   └── hero-video.md
└── assets/
    ├── fleet-architecture.mp4
    └── fleet-architecture.png
```

---

Built around [Hermes Agent](https://github.com/NousResearch/hermes-agent) by [@iacker](https://github.com/iacker).
