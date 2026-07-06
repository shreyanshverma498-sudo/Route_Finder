# Route Finder

## Overview

Route Finder is a graph-based pathfinding application that computes the shortest route between two locations using the **A*** search algorithm. The project uses real-world road network data extracted from **OpenStreetMap** with **OSMnx**, preprocesses the data in Python, and performs route computation using **SWI-Prolog**.

The implementation demonstrates the complete workflow of transforming geographic data into a graph representation and applying heuristic search to determine the optimal path.

---

## Technologies Used

* Python
* SWI-Prolog
* OSMnx
* NetworkX
* Pandas

---

## Project Workflow

1. Define the target region (Chembur, Mumbai).
2. Extract the road network from OpenStreetMap using OSMnx.
3. Preprocess and clean node and edge data.
4. Export the processed graph into CSV files.
5. Load the graph into SWI-Prolog.
6. Execute the A* search algorithm.
7. Reconstruct the shortest path.
8. Export the computed route to `path.csv`.

---

## Project Structure

```text
Route_Finder/
│── City_Graph.py
│── loader.pl
│── astar.pl
│── chembur_nodes.csv
│── chembur_edges.csv
│── prolog_nodes.csv
│── prolog_edges.csv
│── path.csv
│── README.md
```

---

## Algorithm

The project implements the **A*** search algorithm.

For each node:

* **g(n)** represents the distance travelled from the source.
* **h(n)** estimates the remaining distance to the destination using the Euclidean heuristic.
* **f(n) = g(n) + h(n)** determines the next node to explore.

The algorithm terminates once the destination is reached and reconstructs the optimal path.

---

## Running the Project

### Prerequisites

* Python 3.x
* SWI-Prolog

### Install Dependencies

```bash
pip install osmnx networkx pandas matplotlib
```

### Generate Graph Data

```bash
python City_Graph.py
```

### Load the Graph

Inside SWI-Prolog:

```prolog
?- [loader].
```

Run the A* query by specifying the required source and destination nodes.

---

## Output

The computed shortest path is exported as `path.csv`, containing the sequence of nodes representing the optimal route.

---

## Future Improvements

* Interactive user interface
* Map-based visualization
* Support for multiple routing algorithms
* Traffic-aware route planning
* Turn-by-turn navigation

---

## Author

**Shreyansh Verma**

GitHub: https://github.com/shreyanshverma498-sudo
