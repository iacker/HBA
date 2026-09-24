<div align="center">

# ⚔️ Hermes Berserk Armor

**The armor is the infra. Many bodies, one will.**

*One Hermes agent. Several bodies across a fleet. A full plate of self-built tools wrapped around a memory core.*

![fleet architecture](assets/fleet-architecture.png)

</div>

---

## The metaphor

In *Berserk*, the Berserker Armor lets its bearer fight far past human limits — every plate, chain and spike serves the will inside it. This repo is that armor, made real for a **Hermes agent fleet**:

| Berserk | Here |
|---|---|
| **The will inside** | the Hermes agent (the model — the *brain*) |
| **The skeleton / body** | the **harness** it runs on (k3s cluster, Azure node, local Mac) |
| **The beating heart** | the **memory core** — brain-rag + mem0 / pgvector |
| **The plates & chains** | the **tools** — attack, defense, control |
| **Many bodies, one will** | the same agent projected across the whole **fleet** |

The armor decides what the agent can *reach* and what it is *protected from* — never what the will inside it wants.

---

## The fleet — many bodies

The same Hermes will wears the armor on three bodies:

- **Hermes · Azure** — cloud body, always reachable
- **Hermes · k3s** — the harness cluster (`Harness-Cluster`, GitOps via Flux, 24/7)
- **Hermes · Local** — this Mac, hardware-gated, always on

---

## The plates — every tool is a piece of armor

### 🫀 Memory core (the heart)
| Tool | Role |
|---|---|
| [`brain-rag-server`](https://github.com/iacker/brain-rag-server) | Local hybrid-RAG MCP server over an Obsidian vault (embeddings + BM25 + RRF). Zero cloud. |
| **mem0 / pgvector** | Persistent long-term agent memory — facts & preferences that survive every restart. |

### 🗡️ Attack (reach — the sword arm)
| Tool | Role |
|---|---|
| [`ab-live`](https://github.com/iacker/ab-live) | The agent drives *your real browser* — cookies, sessions, extensions — live in the Hermes pane. |
| [`mcp-scalpel`](https://github.com/iacker/mcp-scalpel) | Semantic filter proxy for the Docker MCP Gateway. Cuts catalog tokens 35–52% per turn. |
| **agent-reach** | Eyes on the whole internet — search, extract, act. |

### 🛡️ Defense (the plates & seals)
| Tool | Role |
|---|---|
| [`heucat`](https://github.com/iacker/heucat) | Touch ID-gated secrets, keys sealed in the Apple Secure Enclave. No plaintext `.env`. |
| [`hermes-chthonios`](https://github.com/iacker/hermes-chthonios) | Seal a profile at rest — the agent can encrypt but *physically cannot decrypt* without a YubiKey. |
| [`hermes-argus`](https://github.com/iacker/hermes-argus) | Read-only security auditor — honest scoring, live port checks, plain-language findings. |

### 👁️ Control (the helm)
| Tool | Role |
|---|---|
| [`KubeShip`](https://github.com/iacker/KubeShip) | Pilot your Kubernetes fleet as a game — the infra, made visual and steerable. |

---

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full diagram and data-flow.

The animated fleet schematic lives in [`assets/fleet-architecture.mp4`](assets/fleet-architecture.mp4).

---

## Repo layout

```
hermes-berserk-armor/
├── README.md                    # you are here
├── assets/
│   ├── fleet-architecture.mp4   # animated schematic
│   ├── fleet-architecture.png   # still poster
│   └── reference-berserk-armor.jpg
├── prompts/
│   └── seedance-hero.md         # cinematic video prompt (Seedance / Kling / Runway)
└── docs/
    └── ARCHITECTURE.md          # full architecture write-up
```

---

<div align="center">

*Built around [Hermes Agent](https://github.com/NousResearch/hermes-agent) by [@iacker](https://github.com/iacker).*

**Many bodies. One will.**

</div>
