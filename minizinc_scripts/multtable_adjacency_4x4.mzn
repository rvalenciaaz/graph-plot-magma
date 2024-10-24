include "alldifferent.mzn";

% Define the size of the set and the operation
int: size = 4;
set of int: Elements = 0..size-1;

% Binary operation table ◇
array[Elements, Elements] of var Elements: op;

% Adjacency matrix of the directed graph
array[Elements, Elements] of var 0..1: adj;

% Construct adjacency matrix based on the binary operation table
constraint
    forall(i in Elements, j in Elements)(
        let { var Elements: k = op[i, j] } in
        adj[i, k] = 1 /\ adj[k, j] = 1
    );

% In-degree equals out-degree for every node (Balanced graph condition)
constraint
    forall(i in Elements)(
        sum(j in Elements)(adj[i, j]) = sum(j in Elements)(adj[j, i])
    );

% New constraint: First two elements of the diagonal must be 1
%constraint
%    adj[0, 0] = 1 /\ adj[1, 1] = 1 /\ adj[2, 2] = 1 /\ adj[3, 3] = 1;

% Original operation constraint: x = ((y ◇ z) ◇ x) ◇ (x ◇ y)
constraint
    forall(x in Elements, y in Elements, z in Elements)(
        x = op[op[op[y, z], x], op[x, y]]
    );

% Solve and output the operation table
solve satisfy;

% Output the operation table and adjacency matrix
output [
    "Operation Table:\n",
    "[" ++ concat([ "[" ++ concat([ show(op[i,j]) ++ if j == size-1 then "" else "," endif | j in Elements]) ++ "]"
        ++ if i == size-1 then "" else "," endif | i in Elements ]) ++ "]\n\n",
    "Adjacency Matrix:\n",
    "[" ++ concat([ "[" ++ concat([ show(adj[i,j]) ++ if j == size-1 then "" else "," endif | j in Elements]) ++ "]"
        ++ if i == size-1 then "" else "," endif | i in Elements ]) ++ "]"
];
