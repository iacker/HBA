#!/usr/bin/env python3
"""Generate the memory architecture diagrams for this agent.

Requires only Graphviz (`dot`) on PATH. No Python dependencies, deliberately:
the diagrams must be regenerable years from now from a checkout and a package
manager, without resolving a dependency tree.

Every figure in these diagrams is a local measurement against the agent's real
conversation history and note vault. Measured 2 October 2026.

    python3 memory_diagram.py            # writes the PNGs next to this script
    python3 memory_diagram.py --svg      # also emit SVG
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

BG = "#15171a"
FG = "#e6e8ea"
MUTED = "#9aa3ab"
BORDER = "#333a41"
GOOD_BG, GOOD_LINE = "#17301f", "#3fa66a"
WARN_BG, WARN_LINE = "#32280f", "#d9a21b"
BAD_BG, BAD_LINE = "#301715", "#c2453f"
NEUT_BG, NEUT_LINE = "#1e2125", "#5a636b"
ACCENT = "#6aa9d9"

FONT = "Helvetica"

PREAMBLE = f"""
  bgcolor="{BG}";
  fontname="{FONT}";
  fontcolor="{FG}";
  node [fontname="{FONT}", fontcolor="{FG}", color="{BORDER}",
        style="filled,rounded", shape=box, penwidth=1.4, margin="0.18,0.11"];
  edge [fontname="{FONT}", fontcolor="{MUTED}", color="{BORDER}",
        penwidth=1.3, arrowsize=0.75, fontsize=9];
"""


def layer(name: str, title: str, lines: list[str], bg: str, line: str,
          score: str = "") -> str:
    """One memory layer, rendered as an HTML-like label."""
    body = "".join(
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">{t}</font></td></tr>'
        for t in lines
    )
    sc = (
        f'<tr><td align="left"><font point-size="10" color="{line}">'
        f"<b>{score}</b></font></td></tr>"
        if score
        else ""
    )
    return (
        f'  {name} [fillcolor="{bg}", color="{line}", label=<'
        f'<table border="0" cellborder="0" cellspacing="1">'
        f'<tr><td align="left"><font point-size="11"><b>{title}</b></font></td></tr>'
        f"{body}{sc}</table>>];\n"
    )


# ---------------------------------------------------------------------------
# Figure 1: the five stores, with write path, read path and measured cost
# ---------------------------------------------------------------------------
def fig_architecture() -> str:
    g = ["digraph memory {", PREAMBLE, '  rankdir=TB; nodesep=0.34; ranksep=0.52;',
         '  compound=true;',
         f'  labelloc="t"; fontsize=15;',
         f'  label=<<font point-size="15"><b>Agent memory: five stores, '
         f'one felt memory</b></font><br/>'
         f'<font point-size="10" color="{MUTED}">every number is a local '
         f'measurement, not a vendor benchmark · 2 Oct 2026</font><br/> >;',
         ]

    g.append(
        f'  turn [fillcolor="{NEUT_BG}", color="{ACCENT}", shape=box, '
        f'label=<<font point-size="12"><b>one conversation turn</b></font>>];\n'
    )

    # --- write path -------------------------------------------------------
    g.append(f'  subgraph cluster_w {{\n    label=<<font point-size="11" '
             f'color="{MUTED}"><b>WRITE PATH</b></font>>; '
             f'color="{BORDER}"; style=dashed; fontname="{FONT}";\n')
    writes = [
        ("w1", "self-edit", ["agent rewrites its own", "identity files"]),
        ("w2", "curate", ["human-reviewed note", "into the vault"]),
        ("w3", "append", ["timestamped message,", "verbatim, no LLM"]),
        ("w4", "extract", ["one LLM call per write", "gpt-oss-120b"]),
        ("w5", "author", ["procedure written", "by hand, versioned"]),
    ]
    for n, t, ls in writes:
        bg, ln = (WARN_BG, WARN_LINE) if n == "w4" else (NEUT_BG, NEUT_LINE)
        g.append(layer(n, t, ls, bg, ln))
    g.append("  }\n")

    # --- stores -----------------------------------------------------------
    g.append(f'  subgraph cluster_s {{\n    label=<<font point-size="11" '
             f'color="{MUTED}"><b>FIVE STORES</b></font>>; '
             f'color="{BORDER}"; style=dashed; fontname="{FONT}";\n')
    stores = [
        ("s1", "1 · identity", ["two markdown files",
                                "92% and 97% full",
                                "no forgetting mechanism"], WARN_BG, WARN_LINE),
        ("s2", "2 · curated knowledge", ["hybrid RAG over a vault",
                                         "927 notes, 9 328 chunks",
                                         "BM25 + dense + rerank"], GOOD_BG, GOOD_LINE),
        ("s3", "3 · episodic", ["SQLite FTS5",
                                "9 179 messages",
                                "zero vectors, zero LLM"], GOOD_BG, GOOD_LINE),
        ("s4", "4 · temporal graph", ["fact graph + Postgres",
                                      "531 facts, 28 213 edges",
                                      "45 edges per fact"], BAD_BG, BAD_LINE),
        ("s5", "5 · procedural", ["278 versioned skills",
                                  "loaded on match",
                                  "never benchmarked"], NEUT_BG, NEUT_LINE),
    ]
    for n, t, ls, bg, ln in stores:
        g.append(layer(n, t, ls, bg, ln))
    g.append("  }\n")

    # --- read path --------------------------------------------------------
    g.append(f'  subgraph cluster_r {{\n    label=<<font point-size="11" '
             f'color="{MUTED}"><b>READ PATH, WITH MEASURED COST</b></font>>; '
             f'color="{BORDER}"; style=dashed; fontname="{FONT}";\n')
    reads = [
        ("r1", "injected every turn", ["not selective,",
                                       "never decays"], WARN_BG, WARN_LINE, "0 ms"),
        ("r2", "hybrid + rerank", ["heterogeneous corpus,",
                                   "dense earns its place"], GOOD_BG, GOOD_LINE,
         "MRR 0.858"),
        ("r3", "lexical only", ["nothing tested beat it",
                                "on this corpus"], GOOD_BG, GOOD_LINE,
         "MRR 0.623 · 2 ms"),
        ("r4", "graph + rerank", ["finds no question the",
                                  "others miss"], BAD_BG, BAD_LINE,
         "MRR 0.125 · 31 s"),
        ("r5", "by name or keyword", ["no public benchmark",
                                      "covers this layer"], NEUT_BG, NEUT_LINE,
         "unmeasured"),
    ]
    for n, t, ls, bg, ln, sc in reads:
        g.append(layer(n, t, ls, bg, ln, sc))
    g.append("  }\n")

    g.append(
        f'  ctx [fillcolor="{NEUT_BG}", color="{ACCENT}", '
        f'label=<<font point-size="12"><b>context of the next turn</b></font>>];\n'
    )

    for i in range(1, 6):
        g.append(f"  turn -> w{i} [color=\"{BORDER}\"];\n")
        g.append(f"  w{i} -> s{i};\n")
        g.append(f"  s{i} -> r{i};\n")
        g.append(f"  r{i} -> ctx [color=\"{BORDER}\"];\n")

    g.append("}\n")
    return "".join(g)


# ---------------------------------------------------------------------------
# Figure 2: the bench that decided the episodic engine
# ---------------------------------------------------------------------------
def fig_bench() -> str:
    g = ["digraph bench {", PREAMBLE,
         '  rankdir=LR; nodesep=0.3; ranksep=0.65;',
         f'  labelloc="t"; fontsize=15;',
         f'  label=<<font point-size="15"><b>Why episodic recall stayed on plain '
         f'SQLite FTS5</b></font><br/>'
         f'<font point-size="10" color="{MUTED}">25 questions with verified source '
         f'messages · four configurations · same harness</font><br/> >;',
         ]

    g.append(
        f'  q [fillcolor="{NEUT_BG}", color="{ACCENT}", '
        f'label=<<font point-size="11"><b>question in</b></font><br/>'
        f'<font point-size="11"><b>natural language</b></font>>];\n'
    )
    g.append(layer("lex", "lexical FTS5", ["exact identifiers:",
                                           "versions, paths, PIDs"], GOOD_BG,
                   GOOD_LINE, "2 ms"))
    g.append(layer("den", "dense e5-small", ["384 dim, 5 848 chunks",
                                             "ONNX, no torch"], BAD_BG, BAD_LINE,
                   "11 ms"))
    g.append(layer("rrf", "RRF fusion", ["k = 60"], NEUT_BG, NEUT_LINE, "18 ms"))
    g.append(layer("rr", "cross-encoder", ["ms-marco-MiniLM-L-12",
                                           "0.12 GB, Apache-2.0"], NEUT_BG,
                   NEUT_LINE, "2 244 ms"))

    verdicts = [
        ("v1", "MRR 0.623", ["Hit@1 56% · R@10 80%", "coverage 20/25"],
         GOOD_BG, GOOD_LINE, "KEPT"),
        ("v2", "MRR 0.111", ["Hit@1 8% · R@10 24%", "coverage 6/25"],
         BAD_BG, BAD_LINE, "rejected"),
        ("v3", "MRR 0.512", ["Hit@1 44% · R@10 68%", "coverage 17/25"],
         BAD_BG, BAD_LINE, "rejected"),
        ("v4", "MRR 0.510", ["Hit@1 40% · R@10 84%", "coverage 21/25"],
         BAD_BG, BAD_LINE, "rejected"),
    ]
    for n, t, ls, bg, ln, sc in verdicts:
        g.append(layer(n, t, ls, bg, ln, sc))

    g.append("  q -> lex; q -> den;\n")
    g.append("  lex -> rrf; den -> rrf; rrf -> rr;\n")
    g.append(f'  lex -> v1 [style=bold, color="{GOOD_LINE}"];\n')
    g.append("  den -> v2; rrf -> v3; rr -> v4;\n")

    # the explanation, as a side note
    g.append(
        f'  why [fillcolor="{BG}", color="{BAD_LINE}", shape=box, style="filled", '
        f'label=<<table border="0" cellborder="0" cellspacing="2">'
        f'<tr><td align="left"><font point-size="11" color="{BAD_LINE}">'
        f"<b>why dense loses here</b></font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"similarity over 5 848 chunks:</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{FG}">'
        f"median 0.807 · max 0.878 · min 0.744</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"the whole corpus fits in 0.13 points, and</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"best-to-p99 is 0.014 to 0.035, so ~60</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"passages are indistinguishable from the</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"right one. A technical history is</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"semantically homogeneous: concepts do not</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"discriminate, exact identifiers do.</font></td></tr>"
        f"</table>>];\n"
    )
    g.append(f'  v2 -> why [style=dotted, color="{BAD_LINE}", arrowhead=none];\n')

    # the one remaining lever
    g.append(
        f'  lever [fillcolor="{BG}", color="{GOOD_LINE}", shape=box, style="filled", '
        f'label=<<table border="0" cellborder="0" cellspacing="2">'
        f'<tr><td align="left"><font point-size="11" color="{GOOD_LINE}">'
        f"<b>the one remaining lever</b></font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"a lexical oracle built from answer keywords</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{FG}">'
        f"hits rank 1 in 37 of 37 cases</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"so storage was never the bottleneck. Every</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"failure is a query or ranking failure, and</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"another store cannot help. Fix: put the</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"question vocabulary into the index at write</font></td></tr>"
        f'<tr><td align="left"><font point-size="9" color="{MUTED}">'
        f"time. Costs nothing per query.</font></td></tr>"
        f"</table>>];\n"
    )
    g.append(f'  v1 -> lever [style=dotted, color="{GOOD_LINE}", arrowhead=none];\n')

    g.append("}\n")
    return "".join(g)


FIGURES = {
    "memory-architecture": fig_architecture,
    "memory-bench": fig_bench,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outdir", default=str(Path(__file__).resolve().parent))
    ap.add_argument("--svg", action="store_true", help="also emit SVG")
    args = ap.parse_args()

    if not shutil.which("dot"):
        print("graphviz is required: brew install graphviz", file=sys.stderr)
        return 1

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    formats = ["png"] + (["svg"] if args.svg else [])

    for name, build in FIGURES.items():
        src = out / f"{name}.dot"
        src.write_text(build(), encoding="utf-8")
        for fmt in formats:
            target = out / f"{name}.{fmt}"
            cmd = ["dot", f"-T{fmt}", "-Gdpi=144", str(src), "-o", str(target)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"{name}.{fmt} FAILED\n{r.stderr}", file=sys.stderr)
                return 1
            print(f"  {target.name}  {target.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
