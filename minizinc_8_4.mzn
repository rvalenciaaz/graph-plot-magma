include "alldifferent.mzn";

int: n = 16;  % number of vertices
array[1..n, 1..n] of var 0..1: adj;  % adjacency matrix

array[1..n] of int: out_degrees = [8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 4, 4, 4, 4];  % desired out-degrees
array[1..n] of int: in_degrees  = [8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 4, 4, 4, 4];  % desired in-degrees

% Out-degree constraints: Sum of rows in adjacency matrix must match out_degrees
constraint
    forall(i in 1..n) (
        sum(j in 1..n) (adj[i,j]) = out_degrees[i]
    );

% In-degree constraints: Sum of columns in adjacency matrix must match in_degrees
constraint
    forall(j in 1..n) (
        sum(i in 1..n) (adj[i,j]) = in_degrees[j]
    );

% No self-loops: A vertex can't have an edge to itself
constraint
    forall(i in 1..n) (
        adj[i,i] = 0
    );

solve satisfy;

% Output the adjacency matrix as a list of lists
output [
    show([adj[i,j] | j in 1..n]) ++ if i < n then "\n" else "" endif
    | i in 1..n
];