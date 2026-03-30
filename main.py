#!/usr/bin/env python3
# main.py - run experiments for D3 submission
# runs all 4 algorithms on 3 scenarios (K=2,4,6)
# prints comparison tables and generates data for the HTML visualization

import json, os
from graph import Graph, node_names, short, edges_list, positions
from orders import get_easy, get_medium, get_hard, init_state, h1, h2, combined_h
from search import run_bfs, run_dfs, run_astar, run_ida_star


def print_path(path):
    return " -> ".join(short[n] for n in path)


def run_one_scenario(name, orders, start_node, end_node, graph):
    print(f"\n{'='*65}")
    print(f"  {name}  |  K={len(orders)}  |  Start: {short[start_node]}  |  End: {short[end_node]}")
    order_str = "  ".join(f"[{i}] {short[o.pickup]}->{short[o.delivery]}" for i, o in enumerate(orders))
    print(f"  Orders: {order_str}")
    print(f"{'='*65}")

    algos = [
        ("BFS", run_bfs),
        ("DFS", run_dfs),
        ("A*", run_astar),
        ("IDA*", run_ida_star),
    ]

    results = []
    for algo_name, algo_fn in algos:
        print(f"\n--- {algo_name} ---")
        r = algo_fn(graph, orders, start_node, end_node)
        results.append(r)

        if r["cost"] < 0:
            print("  NO SOLUTION")
            continue
        print(f"  Cost:      {r['cost']} m")
        print(f"  Hops:      {len(r['path'])} nodes")
        print(f"  Expanded:  {r['expanded']}")
        print(f"  Generated: {r['generated']}")
        print(f"  Frontier:  {r['frontier_max']}")
        print(f"  Time:      {r['time_ms']} ms")
        print(f"  Route:     {print_path(r['path'])}")

    return results


def print_summary(all_data):
    print(f"\n{'='*65}")
    print("  COMPARISON TABLE")
    print(f"{'='*65}")

    hdr = f"{'Scenario':<14}{'Algo':<6}{'Cost':>7}{'Expanded':>10}{'Generated':>11}{'Frontier':>10}{'Time':>10}"
    print(hdr)
    print("-" * len(hdr))

    for scenario_name, results in all_data:
        for r in results:
            c = str(r["cost"]) if r["cost"] >= 0 else "N/A"
            t = f"{r['time_ms']}ms" if r["time_ms"] < 1000 else f"{r['time_ms']/1000:.1f}s"
            print(f"{scenario_name:<14}{r['algo']:<6}{c:>7}{r['expanded']:>10}"
                  f"{r['generated']:>11}{r['frontier_max']:>10}{t:>10}")
        print("-" * len(hdr))


def print_d2_comparison(all_data):
    """compare actual results with what we predicted in D2"""
    print(f"\n{'='*65}")
    print("  D2 PREDICTIONS vs D3 ACTUAL")
    print(f"{'='*65}")

    # these numbers are from D2 section 7
    predicted = {
        "Easy (K=2)": {"BFS": "~500", "DFS": "~500", "A*": "~270", "IDA*": "~50-100"},
        "Medium (K=4)": {"BFS": "~5400", "DFS": "~5400", "A*": "~1500", "IDA*": "~500-1500"},
        "Hard (K=6)": {"BFS": "~90000", "DFS": "~90000", "A*": "~4500", "IDA*": "~10k-50k"},
    }

    for (sc_name, results), (pred_name, preds) in zip(all_data, predicted.items()):
        print(f"\n  {pred_name}")
        print(f"  {'Algo':<6}  {'D2 Predicted':>16}  {'D3 Actual':>12}  {'Cost':>8}")
        for r in results:
            p = preds.get(r["algo"], "?")
            c = f"{r['cost']}m" if r["cost"] >= 0 else "N/A"
            print(f"  {r['algo']:<6}  {p:>16}  {r['expanded']:>12}  {c:>8}")


def make_viz_json(graph, all_data, scenarios_info):
    """create the JSON blob for the HTML visualization"""
    nodes_json = []
    for i in range(26):
        x, y = positions[i]
        nodes_json.append({
            "id": i, "name": node_names[i], "short": short[i],
            "role": "pickup" if i in {3,9,10,22,25} else "dropoff",
            "x": x, "y": y
        })

    edges_json = [{"u": u, "v": v, "w": w} for u, v, w in edges_list]

    scenarios_json = []
    for (sc_name, results), (orders, start, dest) in zip(all_data, scenarios_info):
        sc = {
            "name": sc_name,
            "k": len(orders),
            "start": start,
            "dest": dest,
            "orders": [{"pickup": o.pickup, "delivery": o.delivery} for o in orders],
            "results": []
        }
        for r in results:
            # only keep first 200 trace entries (for file size)
            trace_nodes = [s[0] for s in r["trace"][:200]]
            sc["results"].append({
                "algorithm": r["algo"],
                "path": r["path"],
                "cost": r["cost"],
                "expanded": r["expanded"],
                "generated": r["generated"],
                "frontier": r["frontier_max"],
                "time_ms": r["time_ms"],
                "trace": trace_nodes,
            })
        scenarios_json.append(sc)

    return {"nodes": nodes_json, "edges": edges_json, "scenarios": scenarios_json}


def main():
    graph = Graph()
    print(f"Loaded campus graph: 26 nodes, {len(edges_list)} edges")
    print("Floyd-Warshall done.")

    # sanity check - make sure graph is connected
    for i in range(26):
        for j in range(26):
            if graph.shortest_dist(i, j) >= float('inf'):
                print(f"ERROR: nodes {i} and {j} are disconnected!")
                return
    print("Connectivity check: passed\n")

    # define our 3 test scenarios
    # start and end at Malviya (node 8) for all of them
    start_node = 8
    end_node = 8

    test_cases = [
        ("Easy (K=2)",   get_easy()),
        ("Medium (K=4)", get_medium()),
        ("Hard (K=6)",   get_hard()),
    ]

    all_data = []
    scenarios_info = []
    for name, orders in test_cases:
        results = run_one_scenario(name, orders, start_node, end_node, graph)
        all_data.append((name, results))
        scenarios_info.append((orders, start_node, end_node))

    print_summary(all_data)
    print_d2_comparison(all_data)

    # save visualization data
    viz = make_viz_json(graph, all_data, scenarios_info)
    outfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "viz_data.json")
    with open(outfile, "w") as f:
        json.dump(viz, f)
    print(f"\nSaved viz data to {outfile}")

    return viz


if __name__ == "__main__":
    main()
