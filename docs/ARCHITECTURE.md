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
 |   heucat     |<---------| MEMORY (5 tiers) |-------->|  mcp-scalpel |
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

Full measured breakdown, with per-layer cost and the engines that were tested
and rejected: [MEMORY.md](MEMORY.md).

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
   | two self-edited md files    |  stable user facts + preferences
   | 92% and 97% full, no decay  |  injected whole, every turn, 0 ms
   +--------------+--------------+
                  |
      need more?  |  retrieve on demand (narrowest bounded lookup)
                  v
   +--------------+--------------+   +-----------------------------+
   | EPISODIC                    |   | SEMANTIC                    |
   | SQLite FTS5 over 9,179 msgs |   | brain-rag hybrid over the    |
   | lexical only, no vectors    |   | vault: BM25 + dense + rerank |
   | MRR 0.623 in 2 ms, no LLM   |   | MRR 0.858, no LLM            |
   +-----------------------------+   +-----------------------------+
                  |
                  v
   +-----------------------------+   +-----------------------------+
   | TEMPORAL GRAPH (on probation)|   | PROCEDURAL                  |
   | 531 facts, 28k edges, Postgres|  | 278 versioned skills         |
   | MRR 0.125 in 31 s, 1 LLM/write|  | loaded on match, never benched|
   +-----------------------------+   +-----------------------------+
```

- **Working** answers "what are we doing right now" and keeps a long session
  inside the context window.
- **Identity** answers "who is this user, what do they always want" and is
  injected every turn for free. It is also the only layer with no forgetting
  mechanism, so it is the one guaranteed to overflow.
- **Episodic** answers "what happened in a past session". Lexical search alone
  beat every hybrid and reranked variant tested against it, at 2 ms and zero
  tokens.
- **Semantic** answers "what do I know about this topic" from the indexed vault.
  This is where the dense branch earns its place, because a vault is
  heterogeneous while a conversation history is not.
- **Temporal graph** answers "which fact superseded which, and when". Measured
  as a narrow reranker rather than a source: it finds no question the other
  layers miss, for 31 s of latency and one LLM call per write.
- **Procedural** answers "how do I do this kind of task", and is the layer no
  public benchmark covers.

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
| Core (memory) | hermes-lcm, self-edited identity files, SQLite FTS5, brain-rag, temporal fact graph, versioned skills | one felt memory, right store per question, each one benchmarked |
| Reach | mcp-scalpel, ab-live, excalibur, Mando, domain MCP | act on the real world, efficiently |
| Defense | heucat, hermes-chthonios, hermes-argus | power without an exploitable secret |
| Control | KubeShip | see and steer the infrastructure |

## Design principle

Maximise capability, bound the blast radius. Controls never limit what the agent
is meant to do; they limit what an attacker could achieve if the agent were
compromised. Secrets live in hardware, profiles can be sealed so a compromised
agent cannot read a key, and an independent read-only auditor continuously grades
real exposure.
