# Diagrams

Regenerate everything:

```sh
brew install graphviz          # the only dependency
python3 memory_diagram.py --svg
```

`memory_diagram.py` has no Python dependencies on purpose. It emits Graphviz DOT
and shells out to `dot`, so the figures stay regenerable from a checkout and a
package manager, without resolving a dependency tree that will have rotted by
the time anyone needs to edit them. The `.dot` sources are committed alongside
the images so a reviewer can diff the structure, not just the pixels.

| File | What it shows |
|---|---|
| `memory-architecture.png` | the five stores, the write path, and the measured cost of each read path |
| `memory-bench.png` | the four retrieval configurations compared on one bench, and why the cheapest won |

Every number in the figures is a local measurement against this agent's real
conversation history and note vault, dated 2 October 2026. None of it is a
vendor benchmark. The written analysis is in [../MEMORY.md](../MEMORY.md).

Colour is load-bearing: green is measured and kept, red is measured and
rejected, amber is a known unresolved defect, grey is unmeasured.
