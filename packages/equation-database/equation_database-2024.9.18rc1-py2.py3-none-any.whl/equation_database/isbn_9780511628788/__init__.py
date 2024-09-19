import sympy
from equation_database.util.doc import bib, equation
from equation_database.util.parse import frac


@equation()
def table_7_1_qqp_qqp(s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u")):
    """
    $qq' \\to qq'$

    The invariant matrix elements squared for two-to-two parton subprocesses with massless partons. The colour and spin indices are averaged (summed) over initial (final) states.

    Args:
        s: Mandelstam variable s
        t: Mandelstam variable t
        u: Mandelstam variable u
    """
    return frac("4/9") * (s**2 + u**2) / (t**2)


@equation()
def table_7_1_qqpb_qqpb(s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u")):
    """
    $q\\bar{q}' \\to q\\bar{q}'$

    The invariant matrix elements squared for two-to-two parton subprocesses with massless partons. The colour and spin indices are averaged (summed) over initial (final) states.



    Args:
        s: Mandelstam variable s
        t: Mandelstam variable t
        u: Mandelstam variable u
    """
    return frac("4/9") * (s**2 + u**2) / (t**2)


@equation()
def table_7_1_qq_qq(s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u")):
    """
    $qq \\to qq$

    The invariant matrix elements squared for two-to-two parton subprocesses with massless partons. The colour and spin indices are averaged (summed) over initial (final) states.



    Args:
        s: Mandelstam variable s
        t: Mandelstam variable t
        u: Mandelstam variable u
    """
    return frac("4/9") * ((s**2 + u**2) / (t**2) + (s**2 + t**2) / (u**2)) - frac(
        "8/27"
    ) * s**2 / (u * t)


@equation()
def table_7_1_qqb_qpqpb(s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u")):
    """
    $q\\bar{q} \\to q'\\bar{q}'$

    The invariant matrix elements squared for two-to-two parton subprocesses with massless partons. The colour and spin indices are averaged (summed) over initial (final) states.



    Args:
        s : Mandelstam variable s
        t : Mandelstam variable t
        u : Mandelstam variable u

    """
    return frac("4/9") * ((t**2 + u**2) / (s**2))


@equation()
def table_7_1_qqb_qqb(s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u")):
    """
    $q\\bar{q} \\to q\\bar{q}$

    The invariant matrix elements squared for two-to-two parton subprocesses with massless partons. The colour and spin indices are averaged (summed) over initial (final) states.



    Args:
        s : Mandelstam variable s
        t : Mandelstam variable t
        u : Mandelstam variable u
    """
    return frac("4/9") * ((s**2 + u**2) / (t**2) + (t**2 + u**2) / (s**2)) - frac(
        "8/27"
    ) * u**2 / (s * t)


@equation()
def table_7_1_qqb_gg(s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u")):
    """
    $q\\bar{q} \\to gg$

    The invariant matrix elements squared for two-to-two parton subprocesses with massless partons. The colour and spin indices are averaged (summed) over initial (final) states.



    Args:
        s : Mandelstam variable s
        t : Mandelstam variable t
        u : Mandelstam variable u
    """
    return frac("32/27") * (t**2 + u**2) / (t * u) - frac("8/3") * (t**2 + u**2) / (
        s**2
    )


@equation()
def table_7_1_gg_qqb(s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u")):
    """
    $gg \\to q\\bar{q}$

    The invariant matrix elements squared for two-to-two parton subprocesses with massless partons. The colour and spin indices are averaged (summed) over initial (final) states.



    Args:
        s : Mandelstam variable s
        t : Mandelstam variable t
        u : Mandelstam variable u
    """
    return frac("1/6") * (t**2 + u**2) / (t * u) - frac("3/8") * (t**2 + u**2) / (s**2)


@equation()
def table_7_1_gq_gq(s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u")):
    """
    $gq \\to gq$

    The invariant matrix elements squared for two-to-two parton subprocesses with massless partons. The colour and spin indices are averaged (summed) over initial (final) states.



    Args:
        s : Mandelstam variable s
        t : Mandelstam variable t
        u : Mandelstam variable u
    """
    return frac("-4/9") * (s**2 + u**2) / (s * u) + (u**2 + s**2) / t**2


@equation()
def table_7_1_gg_gg(s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u")):
    """
    $gg \\to gg$

    The invariant matrix elements squared for two-to-two parton subprocesses with massless partons. The colour and spin indices are averaged (summed) over initial (final) states.



    Args:
        s : Mandelstam variable s
        t : Mandelstam variable t
        u : Mandelstam variable u
    """
    return frac("9/2") * (3 - t * u / s**2 - s * u / t**2 - s * t / u**2)


@equation()
def table_7_2_qq_ag(
    s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u"), N=sympy.Symbol("N")
):
    """$q\\bar q \\to \\gamma^* g$

    Lowest order processes for virtual photon production. The colour and spin indices are averaged (summed) over initial (final) states. For a real photon (s + t + u) = 0 and for SU(3) we have N = 3

    Args:
        s : Mandelstam variable s
        t : Mandelstam variable t
        u : Mandelstam variable u
        N : Number of colors
    """
    return (N**2 - 1) / N**2 * (t**2 + u**2 + 2 * s * (s + t + u)) / (t * u)


@equation()
def table_7_2_gq_aq(
    s=sympy.Symbol("s"), t=sympy.Symbol("t"), u=sympy.Symbol("u"), N=sympy.Symbol("N")
):
    """$gq \\to \\gamma^* q$

    Lowest order processes for virtual photon production. The colour and spin indices are averaged (summed) over initial (final) states. For a real photon (s + t + u) = 0 and for SU(3) we have N = 3

    Args:
        s : Mandelstam variable s
        t : Mandelstam variable t
        u : Mandelstam variable u
        N : Number of colors
    """
    return -1 / N * (s**2 + u**2 + s * t * (s + t + u) / (s * u))


@bib()
def bibtex():
    bibtex: str = """
@book{Ellis:1996mzs,
    author = "Ellis, R. Keith and Stirling, W. James and Webber, B. R.",
    title = "{QCD and collider physics}",
    doi = "10.1017/CBO9780511628788",
    isbn = "978-0-511-82328-2, 978-0-521-54589-1",
    publisher = "Cambridge University Press",
    volume = "8",
    month = "2",
    year = "2011"
}
"""
    return bibtex
