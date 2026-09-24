# Architecture

## Whole system

```
                          +-------------------------------+
                          |        THE FLEET (bodies)     |
                          +-------------------------------+
        +----------------+   +----------------+   +----------------+
        | HERMES · AZURE |---|  HERMES · K3S  |---| HERMES · LOCAL |
        |  cloud node    |   | Harness-Cluster|   |  this Mac      |
        +-------+--------+   +-------+--------+   +-------+--------+
                +--------------------+--------------------+
                                     |  one will, projected across bodies
                                     v
                          +---------------------+
                          |      CONTROL        |
                          |      KubeShip       |  observe + steer the fleet
                          +----------+----------+
                                     |
   DEFENSE                          v                          REACH
 +--------------+          +-----------------+          +--------------+
 |   heucat     |<---------|  MEMORY (4 tiers)|-------->|  mcp-scalpel |
 | enclave keys |          |  working /       |         | token filter |
 +--------------+          |  identity /      |         +--------------+
 |  chthonios   |<---------|  episodic /      |-------->|   ab-live    |
 | seal at rest |          |  semantic        |         | real browser |
 +--------------+          +-----------------+          +--------------+
 | hermes-argus |<------------------------------------->|  excalibur   |
 | live audit   |                                       | scan->report |
 +--------------+                                       +--------------+
```

## Memory tiers (detail)

```
        turn N of a live session
                 |
                 v
   +-----------------------------+  WORKING  (this session)
   | hermes-lcm                  |  compacts the running conversation into a
   | context compaction plugin   |  summary DAG + protected recent tail
   +--------------+--------------+
                  |
                  v
   +-----------------------------+  IDENTITY  (always in context, no lookup)
   | mem0 / pgvector + notes     |  stable user facts + preferences
   +--------------+--------------+
                  |
      need more?  |  retrieve on demand (narrowest bounded lookup)
                  v
   +--------------+--------------+   +-----------------------------+
   | agentmemory                 |   | brain-rag / neuromancer     |
   | EPISODIC: past sessions,    |   | SEMANTIC: hybrid RAG over    |
   | lessons, knowledge graph    |   | the vault (embeddings+BM25)  |
   +-----------------------------+   +-----------------------------+
```

- **Working** answers "what are we doing right now" and keeps a long session
  inside the context window.
- **Identity** answers "who is this user, what do they always want" and is
  injected every turn for free.
- **Episodic** answers "what happened before, what did I learn" and is queried
  on demand.
- **Semantic** answers "what do I know about this topic" from the indexed vault.

## Data flow

1. The agent runs on whichever body is active (Azure, k3s, local).
2. Per turn it consults working + identity memory (already in context), and only
   reaches into episodic or semantic memory when that is insufficient.
3. Reach tools act on the world: `mcp-scalpel` keeps the catalog lean, `ab-live`
   drives the real browser, `excalibur` / `Mando` run security workflows, domain
   MCP servers (`blender`, `vibe-trading`, `erp`) extend reach.
4. Defense bounds the blast radius: `heucat` (enclave keys), `hermes-chthonios`
   (encrypt-only sealing), `hermes-argus` (read-only audit).
5. Control: `KubeShip` steers the fleet, backed by `Harness-Cluster` (Flux CD)
   running the agents 24/7.

## Layers

| Layer | Components | Guarantee |
|-------|-----------|-----------|
| Bodies | Harness-Cluster, Azure node, local | the agent runs 24/7, anywhere |
| Core (memory) | hermes-lcm, mem0/pgvector, agentmemory, brain-rag, neuromancer | one felt memory, right store per question |
| Reach | mcp-scalpel, ab-live, excalibur, Mando, domain MCP | act on the real world, efficiently |
| Defense | heucat, hermes-chthonios, hermes-argus | power without an exploitable secret |
| Control | KubeShip | see and steer the infrastructure |

## Design principle

Maximise capability, bound the blast radius. Controls never limit what the agent
is meant to do; they limit what an attacker could achieve if the agent were
compromised. Secrets live in hardware, profiles can be sealed so a compromised
agent cannot read a key, and an independent read-only auditor continuously grades
real exposure.
