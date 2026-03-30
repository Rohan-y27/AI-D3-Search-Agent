import time

from utils import Order, DeliveryProblem
from algorithms import bfs, dfs, astar, idastar
from graph import path_to_names


def run(algo, problem):
    start = time.time()
    res = algo(problem)
    end = time.time()

    print("\n---", res["algorithm"], "---")
    print("Cost:", res["cost"])
    print("Expanded:", res["expanded"])
    print("Time:", round((end - start) * 1000, 2), "ms")

    if res["path"]:
        print("Path:", path_to_names(res["path"]))
    else:
        print("No path found")


def test_easy():
    print("\n===== EASY (K=1) =====")

    orders = [
        Order(23, 14, 0)
    ]

    problem = DeliveryProblem(orders, start=12, goal=12)

    run(bfs, problem)
    run(dfs, problem)
    run(astar, problem)

    print("\nCalling IDA*...")
    run(idastar, problem)


def test_medium():
    print("\n===== MEDIUM (K=2) =====")

    orders = [
        Order(4, 1, 0),
        Order(11, 24, 1)
    ]

    problem = DeliveryProblem(orders, start=12, goal=12)

    run(bfs, problem)
    run(dfs, problem)
    run(astar, problem)

    print("\nCalling IDA*...")
    run(idastar, problem)


def test_hard():
    print("\n===== HARD (K=3) =====")

    orders = [
        Order(4, 20, 0),
        Order(23, 19, 1),
        Order(10, 3, 2)
    ]

    problem = DeliveryProblem(orders, start=12, goal=12)

    run(bfs, problem)
    run(dfs, problem)
    run(astar, problem)

    print("\nCalling IDA*...")
    run(idastar, problem)


if __name__ == "__main__":
    print("Choose test case:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    choice = input("Enter choice (1/2/3): ")

    if choice == "1":
        test_easy()
    elif choice == "2":
        test_medium()
    elif choice == "3":
        test_hard()
    else:
        print("Invalid choice")