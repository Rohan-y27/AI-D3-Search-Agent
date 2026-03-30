# D3: Implementation & Empirical Analysis
## CS F407 Artificial Intelligence - Group 29

**Members:**
- Raghav Jain (2022A7TS0075P)
- Rohan Yadav (2023A7PS0530P)
- Anant Srivastava (2023A4PS0422P)

## What this is

Implementation of 4 search algorithms (BFS, DFS, A*, IDA*) for the campus food delivery problem from D1/D2. The agent navigates the 26-node BITS Pilani campus graph, picking up food orders and delivering them to hostels.

We use two heuristics from D1:
- h1: MST-based lower bound (Prim's on shortest-path distances)
- h2: Min-edge lower bound (sum of cheapest edges, halved)
- Combined: h = max(h1, h2)

## How to run

```
python main.py          # runs all experiments, prints tables
python gen_viz.py       # generates visualization.html
```

Then open `visualization.html` in a browser for the interactive visualization.

No external packages needed - just Python 3.8+.

## Files

- `graph.py` - campus graph (26 nodes, 41 edges) + Floyd-Warshall
- `orders.py` - order definitions, state transitions, heuristics
- `search.py` - BFS, DFS, A*, IDA*
- `main.py` - runs experiments, prints comparison tables
- `gen_viz.py` - builds the HTML visualization
- `template.html` - visualization template
- `visualization.html` - generated interactive viz (open in browser)

## Test scenarios

| Name | K | Orders |
|------|---|--------|
| Easy | 2 | FM→RAM, DOM→BDH |
| Medium | 4 | FM→SR, DOM→GAN, ANC→VK, LOT→ASH |
| Hard | 6 | FM→RAM, DOM→SR, ANC→VK, LOT→BHG, CNOT→RP, FM→VYS |

All start and end at Malviya Bhawan (node 8).
