# Architecture

```
                          +-------------------------------+
                          |        THE FLEET (bodies)     |
                          +-------------------------------+
        +----------------+   +----------------+   +----------------+
        | HERMES · AZURE |---|  HERMES · K3S  |---| HERMES · LOCAL |
        |  cloud node    |   | Harness-Cluster|   |  this Mac      |
        |  always reach  |   |  Flux / GitOps |   |  always on     |
        +-------+--------+   +-------+--------+   +-------+--------+
                +--------------------+--------------------+
                                     |  (one will, projected across bodies)
                                     v
                          +---------------------+
                          |      CONTROL        |
                          |      KubeShip       |  observe and steer the fleet
                          +----------+----------+
                                     |
   DEFENSE                          v                          REACH
 +--------------+          +-----------------+          +--------------+
 |   heucat     |<---------|   MEMORY CORE   |--------->|  mcp-scalpel |
 | enclave keys |          |                 |          | token filter |
 +--------------+          |   brain-rag     |          +--------------+
 |  chthonios   |<---------| mem0 / pgvector |--------->|   ab-live    |
 | seal at rest |          +-----------------+          | real browser |
 +--------------+                                       +--------------+
 | hermes-argus |<------------------------------------->|  excalibur   |
 | live audit   |                                       | scan -> report|
 +--------------+                                       +--------------+
```

## Data flow

1. The agent (the model) runs on whichever body is active — Azure, k3s, or local.
2. On every turn it queries the memory core: `brain-rag` for vault knowledge
   (hybrid RAG) and `mem0` / `pgvector` for personal facts and preferences. This
   context survives restarts and travels with the agent across bodies.
3. Reach tools extend what it can do: `mcp-scalpel` keeps the tool catalog lean,
   `ab-live` gives it a real browser, `excalibur` and `Mando` handle offensive
   security workflows.
4. Defense tools bound the blast radius: `heucat` (enclave-sealed secrets),
   `hermes-chthonios` (encrypt-only profile sealing), `hermes-argus` (continuous
   read-only audit).
5. Control: `KubeShip` visualises and steers the whole fleet, backed by the
   `Harness-Cluster` GitOps setup running the agents 24/7.

## Layers

| Layer | Components | Guarantee |
|-------|-----------|-----------|
| Bodies | Harness-Cluster, Azure node, local | the agent runs 24/7, anywhere |
| Core | brain-rag-server, mem0 / pgvector, neuromancer-mcp | memory that persists and travels |
| Reach | mcp-scalpel, ab-live, excalibur, Mando | act on the real world, efficiently |
| Defense | heucat, hermes-chthonios, hermes-argus | power without an exploitable secret |
| Control | KubeShip | see and steer the infrastructure |

## Design principle

Maximise capability, bound the blast radius. The controls never limit what the
agent is meant to do — they limit what an attacker could achieve if the agent
were compromised. Secrets live in hardware, profiles can be sealed so that a
compromised agent cannot even read a key, and an independent read-only auditor
continuously grades the real exposure.
