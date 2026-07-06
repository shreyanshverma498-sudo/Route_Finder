:- use_module(library(csv)).

% Load both nodes and edges
load_data(NodesFile, EdgesFile) :-
    load_nodes(NodesFile),
    load_edges(EdgesFile).

% ---------- Load Nodes ----------
load_nodes(File) :-
    csv_read_file(File, Rows, [functor(raw_node), arity(3)]),
    maplist(assert_node, Rows).

assert_node(raw_node(ID, Lat, Lon)) :-
    assert(node(ID, Lat, Lon)).

% ---------- Load Edges ----------
load_edges(File) :-
    csv_read_file(File, Rows, [functor(raw_edge), arity(3)]),
    maplist(assert_edge, Rows).

% Always make bidirectional
assert_edge(raw_edge(U, V, Cost)) :-
    assert(edge(U, V, Cost)),
    assert(edge(V, U, Cost)).
    
