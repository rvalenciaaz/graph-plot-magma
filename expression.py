import sympy as sp

def compute_a_star_and_inverse(n):
    # Define symbolic matrices for `a` and `a_star`
    a = sp.MatrixSymbol('a', n, n)
    a_star = sp.MatrixSymbol('a_star', n, n)

    # Compute a_star from a (Forward process)
    def forward_a_star(a, n):
        equations = []
        for i in range(n):
            for j in range(n):
                i_prime, j_prime = sp.symbols('i_prime j_prime')
                sum_expr = sp.summation(a[i_prime, j_prime], (i_prime, 0, i), (j_prime, 0, j))
                equation = sp.Eq(a_star[i, j], (i + 1) + (j + 1)-1 - sum_expr) #2*
                equations.append(equation)
        
        solution = sp.solve(equations, [a_star[i, j] for i in range(n) for j in range(n)])
        return solution

    # Compute a from a_star (Inverse process)
    def inverse_a_star(a_star, n):
        equations = []
        for i in range(n):
            for j in range(n):
                i_prime, j_prime = sp.symbols('i_prime j_prime')
                sum_expr = sp.summation(a[i_prime, j_prime], (i_prime, 0, i), (j_prime, 0, j))
                equation = sp.Eq(a_star[i, j], (i + 1) + (j + 1)-1 - sum_expr)
                equations.append(equation)
        
        solution = sp.solve(equations, [a[i, j] for i in range(n) for j in range(n)])
        return solution

    # Calculate and display both forward and inverse solutions
    forward_solution = forward_a_star(a, n)
    inverse_solution = inverse_a_star(a_star, n)

    # Display solutions
    print("Forward solution (a_star in terms of a):")
    for key, value in forward_solution.items():
        sp.pprint(f"{key} = {value}")

    print("\nInverse solution (a in terms of a_star):")
    for key, value in inverse_solution.items():
        sp.pprint(f"{key} = {value}")

#Example for n=2
n = 8
compute_a_star_and_inverse(n)
