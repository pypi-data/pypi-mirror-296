import sympy

from equation_database.util.doc import bib, equation

# s = sympy.symbols('s')
# """Mandelstam variable s"""
#
# t = sympy.symbols('t')
# """Mandelstam variable t"""
#
# u = sympy.symbols('u')
# """Mandelstam variable u"""
#
# p1_mu = sympy.symbols('p1_mu')
# p2_mu = sympy.symbols('p2_mu')
# p3_mu = sympy.symbols('p3_mu')
# p4_mu = sympy.symbols('p4_mu')
#
# S_mu = sympy.symbols('S_mu')
# T_mu = sympy.symbols('T_mu')
# U_mu = sympy.symbols('U_mu')


@equation()
def equation_A3(
    S_mu=sympy.Symbol("S_mu"),
    U_mu=sympy.Symbol("U_mu"),
    T_mu=sympy.Symbol("T_mu"),
    p1_mu=sympy.Symbol("p1_mu"),
    p2_mu=sympy.Symbol("p2_mu"),
    p3_mu=sympy.Symbol("p3_mu"),
    p4_mu=sympy.Symbol("p4_mu"),
):
    """
    Mandelstam vectors.

    Args:
        S_mu: S_mu
        U_mu: U_mu
        T_mu: T_mu
        p1_mu: p1_mu
        p2_mu: p2_mu
        p3_mu: p3_mu
        p4_mu: p4_mu
    """
    return (
        sympy.Eq(S_mu, (p1_mu + p2_mu)),
        sympy.Eq(S_mu, (p3_mu + p4_mu)),
        sympy.Eq(U_mu, (p1_mu - p3_mu)),
        sympy.Eq(U_mu, (p4_mu - p2_mu)),
        sympy.Eq(T_mu, (p1_mu - p4_mu)),
        sympy.Eq(T_mu, (p3_mu - p2_mu)),
    )


@equation()
def equation_A4(
    s=sympy.Symbol("s"),
    S_mu=sympy.Symbol("S_mu"),
    t=sympy.Symbol("t"),
    T_mu=sympy.Symbol("T_mu"),
    u=sympy.Symbol("u"),
    U_mu=sympy.Symbol("U_mu"),
):
    """
    Definition of Mandelstam variables in terms of $S_mu$, $T_mu$, and $U_mu$.

    Args:
        s: Mandelstam variable s
        S_mu: S_mu
        t: Mandelstam variable t
        T_mu: T_mu
        u: Mandelstam variable u
        U_mu: U_mu
    """
    return sympy.Eq(s, S_mu**2), sympy.Eq(t, T_mu**2), sympy.Eq(u, U_mu**2)


@bib()
def bibtex():
    bibtex: str = """
@article{Balachandran:1968rj,
    author = "Balachandran, A. P. and Nuyts, J. and Meggs, W. J. and Ramond, Pierre",
    title = "{Simultaneous partial wave expansion in the Mandelstam variables: the group SU(3)}",
    doi = "10.1103/PhysRev.176.1700",
    journal = "Phys. Rev.",
    volume = "176",
    pages = "1700",
    year = "1968"
}
"""
    return bibtex
