:- use_module(library(heaps)).
:- use_module(library(assoc)).
:- use_module(library(csv)).

% ---------- MAIN A* ENTRY ----------
astar(Start, Goal, Path, Cost) :-
    heuristic(Start, Goal, H),
    empty_heap(Open0),
    add_to_heap(Open0, H, node(Start, 0, H, [Start]), Open),
    empty_assoc(GCosts0),
    put_assoc(Start, GCosts0, 0, GCosts),
    astar_loop(Open, Goal, GCosts, RevPath, Cost),
    reverse(RevPath, Path),
    save_path_to_csv(Path, 'path.csv').

% ---------- CORE A* LOOP ----------
astar_loop(Open, Goal, _, Path, Cost) :-
    get_from_heap(Open, _F, node(Goal, G, _, Path), _),
    Cost = G, !.

astar_loop(Open, Goal, GCosts, Path, Cost) :-
    get_from_heap(Open, _F, node(Current, G, _, RevPath), RestOpen),
    findall(
        node(Next, NewG, NewF, [Next|RevPath]),
        (
            edge(Current, Next, StepCost),
            \+ memberchk(Next, RevPath),  % avoid cycles
            NewG is G + StepCost,
            heuristic(Next, Goal, H),
            NewF is NewG + H,
            (   get_assoc(Next, GCosts, OldG) -> NewG < OldG ; true )
        ),
        Successors
    ),
    update_open(Successors, RestOpen, GCosts, NewOpen, NewGCosts),
    astar_loop(NewOpen, Goal, NewGCosts, Path, Cost).

update_open([], Open, GCosts, Open, GCosts).
update_open([node(N, G, F, Path)|Rest], Open0, GCosts0, Open, GCosts) :-
    add_to_heap(Open0, F, node(N, G, F, Path), Open1),
    put_assoc(N, GCosts0, G, GCosts1),
    update_open(Rest, Open1, GCosts1, Open, GCosts).

% ---------- HEURISTIC (Euclidean) ----------
heuristic(Node, Goal, H) :-
    node(Node, Lat1, Lon1),
    node(Goal, Lat2, Lon2),
    DLat is Lat2 - Lat1,
    DLon is Lon2 - Lon1,
    H is sqrt(DLat*DLat + DLon*DLon).

% ---------- SAVE FINAL PATH TO CSV ----------
save_path_to_csv(Path, Filename) :-
    open(Filename, write, Stream),
    format(Stream, 'node_id,lat,lon~n', []),  % header row
    save_nodes(Path, Stream),
    close(Stream).

save_nodes([], _).
save_nodes([ID|Rest], Stream) :-
    node(ID, Lat, Lon),
    format(Stream, '~w,~w,~w~n', [ID, Lat, Lon]),
    save_nodes(Rest, Stream).

