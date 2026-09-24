# Architecture — Hermes Berserk Armor

```
                          ╔═══════════════════════════════╗
                          ║        THE FLEET (bodies)      ║
                          ╚═══════════════════════════════╝
        ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
        │ HERMES · AZURE │───│  HERMES · K3S  │───│ HERMES · LOCAL │
        │  cloud node    │   │ Harness-Cluster│   │  this Mac      │
        │  always reach  │   │  Flux / GitOps │   │  always on     │
        └───────┬────────┘   └───────┬────────┘   └───────┬────────┘
                └────────────────────┼────────────────────┘
                                     │  (same will, projected)
                                     ▼
                          ┌─────────────────────┐
                          │      CONTROL 👁       │
                          │      KubeShip        │  pilot the fleet as a game
                          └──────────┬──────────┘
                                     │
   DEFENSE 🛡                        ▼                        ATTACK 🗡
 ┌──────────────┐          ╔═════════════════╗          ┌──────────────┐
 │   heucat     │◀─────────║   MEMORY CORE   ║─────────▶│   ab-live    │
 │ enclave keys │          ║    (the heart)  ║          │ real browser │
 ├──────────────┤          ║                 ║          ├──────────────┤
 │  chthonios   │◀─────────║   brain-rag     ║─────────▶│ mcp-scalpel  │
 │ seal at rest │          ║ mem0 / pgvector ║          │ token filter │
 ├──────────────┤          ╚═════════════════╝          ├──────────────┤
 │ hermes-argus │◀───────────────────────────────────▶│ agent-reach  │
 │ live audit   │                                       │ internet     │
 └──────────────┘                                       └──────────────┘
```

## Data flow

1. **The will** (model) runs on whichever **body** is active (Azure / k3s / Local).
2. Every turn it queries the **Memory Core** — `brain-rag` (vault knowledge, hybrid RAG) and `mem0/pgvector` (personal facts & preferences) — so context survives restarts and moves with it across bodies.
3. **Attack** tools extend reach: `ab-live` (real browser), `mcp-scalpel` (lean tool catalog), `agent-reach` (search/extract/act).
4. **Defense** tools bound the blast radius: `heucat` (enclave-sealed secrets), `chthonios` (encrypt-only profile sealing), `hermes-argus` (continuous read-only audit).
5. **Control**: `KubeShip` visualizes and steers the whole fleet.

## Layers

| Layer | Repos | Guarantee |
|---|---|---|
| Bodies | Harness-Cluster, Azure node, local | the will runs 24/7, anywhere |
| Heart | brain-rag-server, mem0/pgvector | memory that persists and travels |
| Reach | ab-live, mcp-scalpel, agent-reach | act on the real world, cheaply |
| Guard | heucat, chthonios, hermes-argus | power without an exploitable secret |
| Helm | KubeShip | see and steer the infra |

**Design principle:** maximize capability, cage the blast radius. The armor never limits what the will *wants* — only what an attacker could *do* if it were turned.
