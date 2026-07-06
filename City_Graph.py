import osmnx as ox
import pandas as pd

# Bounding box around Chembur
north, south, east, west = 19.08, 19.03, 72.92, 72.88

print("📍 Downloading Chembur road network...")
G = ox.graph_from_bbox(north, south, east, west, network_type="drive")

# Convert to GeoDataFrames
nodes, edges = ox.graph_to_gdfs(G)

# Keep only node_id, lat, lon
nodes_clean = nodes.reset_index()[['osmid', 'y', 'x']]
nodes_clean.to_csv("prolog_nodes.csv", index=False)

# Keep only u, v, length
edges_clean = edges.reset_index()[['u', 'v', 'length']]
edges_clean.to_csv("prolog_edges.csv", index=False)

print("✅ Cleaned files exported: prolog_nodes.csv & prolog_edges.csv")

