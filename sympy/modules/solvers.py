"""
This module contain solvers for all kinds of equations,
both algebraic (solve) and differential (dsolve).
"""

from sympy import Basic, Symbol, Number, Mul, log, Add, Derivative, \
        sin, cos, integrate, sqrt, exp, Rational

def solve(eq, vars):
    """
    Solves any (supported) kind of equation (not differential).

    Examples
    ================
      >>> from sympy import Symbol
      >>> x, y = Symbol('x'), Symbol('y')
      >>> solve(2*x-3, [x])
      3/2

    """

    #currently only solve for one function
    if isinstance(vars, Symbol) or len(vars) == 1:
        x = vars[0]
        a,b,c = [Symbol(s, is_dummy = True) for s in ["a","b","c"]]

        r = eq.match(a*x + b, [a,b])
        if r and wo(r,x): return solve_linear(r[a], r[b])

        r = eq.match(a*x**2 + c, [a,c])
        if r and wo(r,x): return solve_quadratic(r[a], 0, r[c])

        r = eq.match(a*x**2 + b*x + c, [a,b,c])
        if r and wo(r,x): return solve_quadratic(r[a], r[b], r[c])

    raise "Sorry, can't solve it (yet)."

def solve_linear(a, b):
    return -b/a

def solve_quadratic(a, b, c):
    D = b**2-4*a*c
    if D == 0:
        return [-b/(2*a)]
    else:
        return [
                (-b+sqrt(D))/(2*a),
                (-b-sqrt(D))/(2*a)
               ]

def dsolve(eq, funcs):
    """
    Solves any (supported) kind of differential equation.

    Usage
    =====
    dsolve(3*Derivative(f(x),x)-1, [f(x)])
    x/3+Symbol("C1")

    dsolve(Derivative(Derivative(f(x),x),x)+9*f(x), [f(x)])
    sin(3*x)*C1+cos(3*x)*C2

    Details
    =======

    This function just parses the equation "eq" and determines the type of
    differential equation, then it determines all the coefficients and then
    calls the particular solver, which just accepts the coefficients.

    """

    #currently only solve for one function
    if len(funcs) == 1:
        f = funcs[0]
        x = f[0]
        a,b,c = [Symbol(s, is_dummy = True) for s in ["a","b","c"]]

        r = eq.match(a*Derivative(f,x) + b, [a,b])
        if r and wo(r,f): return solve_ODE_first_order(r[a], r[b], f, x)

        r = eq.match(a*Derivative(Derivative(f,x),x) + b*f, [a,b])
        if r and wo(r,f): return solve_ODE_second_order(r[a], 0, r[b], f, x)

        #special equations, that we know how to solve
        t = x*exp(-f)
        tt = (a*t.diffn(x,2)/t).expand()
        r = eq.match(tt, [a])
        #there is a bug in match(), it should actually return this:
        r = {a: -Rational(1)/2}
        #check, that we've rewritten the equation correctly:
        assert ( t.diffn(x,2)*r[a]/t ).expand() == eq
        return solve_ODE_1(f, x)

    raise "Sorry, can't solve it (yet)."

def solve_ODE_first_order(a, b, f, x):
    """ a*f'(x)+b = 0 """
    return integrate(-b/a, x) + Symbol("C1")

def solve_ODE_second_order(a, b, c, f, x):
    """ a*f''(x) + b*f'(x) + c = 0 """
    #a very special case, for b=0 and a,c not depending on x:
    return Symbol("C1")*sin(sqrt(c/a)*x)+Symbol("C2")*cos(sqrt(c/a)*x)

def solve_ODE_1(f, x):
    """ (x*exp(-f(x)))'' = 0 """
    C1 = Symbol("C1")
    C2 = Symbol("C2")
    return -log(C1+C2/x)


def wo(di, x):
    """Are all items in the dictionary "di" without "x"?"""
    for d in di:
        if di[d].has(x):
            return False
    return True