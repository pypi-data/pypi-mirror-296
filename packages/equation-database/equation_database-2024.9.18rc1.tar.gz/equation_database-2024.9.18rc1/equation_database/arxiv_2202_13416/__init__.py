import sympy

from equation_database.util.doc import bib, equation


@equation()
def equation_2_4(
    M_s=sympy.Symbol("M_s"),
    g_s=sympy.Symbol("g_s"),
    C_A=sympy.Symbol("C_A"),
    C_F=sympy.Symbol("C_F"),
    B=sympy.Symbol("B"),
    s=sympy.Symbol("s"),
    m_X=sympy.Symbol("m_X"),
    t=sympy.Symbol("t"),
):
    """

    Args:
        M_s: Matrix element for the s channel
        g_s: strong coupling constant
        C_A: Casimir operator for the adjoint representation of SU(3)
        C_F: Casimir operator for the fundamental representation of SU(3)
        B: squared eletroweakino-squark coupling
        s: Mandelstam variable s
        m_X: Mass of the electroweakino
        t: Mandelstam variable t
    """
    return sympy.Eq(sympy.Abs(M_s) ** 2, g_s**2 * C_A * C_F * B / s * 2 * (m_X**2 - t))


@equation()
def equation_2_5(
    M_u=sympy.Symbol("M_u"),
    g_s=sympy.Symbol("g_s"),
    C_A=sympy.Symbol("C_A"),
    C_F=sympy.Symbol("C_F"),
    B=sympy.Symbol("B"),
    u=sympy.Symbol("u"),
    m_X=sympy.Symbol("m_X"),
    m_sq=sympy.Symbol("m_sq"),
):
    """


    Args:
        M_u: Matrix element for the u channel
        g_s: strong coupling constant
        C_A: Casimir operator for the adjoint representation of SU(3)
        C_F: Casimir operator for the fundamental representation of SU(3)
        B: squared eletroweakino-squark coupling
        u: Mandelstam variable u
        m_X: Mass of the electroweakino
        m_sq: Mass of the squark
    """
    return sympy.Eq(
        sympy.Abs(M_u) ** 2,
        g_s**2 * C_A * C_F * B / (u - m_sq**2) ** 2 * 2 * (m_X**2 - u) * (m_sq**2 + u),
    )


@equation()
def equation_2_6(
    M_s=sympy.Symbol("M_s"),
    M_u=sympy.Symbol("M_u"),
    g_s=sympy.Symbol("g_s"),
    C_A=sympy.Symbol("C_A"),
    C_F=sympy.Symbol("C_F"),
    B=sympy.Symbol("B"),
    s=sympy.Symbol("s"),
    u=sympy.Symbol("u"),
    m_X=sympy.Symbol("m_X"),
    m_sq=sympy.Symbol("m_sq"),
):
    """

    Args:
        M_s: Matrix element for the s channel
        M_u: Matrix element for the u channel
        g_s: strong coupling constant
        C_A: Casimir operator for the adjoint representation of SU(3)
        C_F: Casimir operator for the fundamental representation of SU(3)
        B: squared eletroweakino-squark coupling
        s: Mandelstam variable s
        u: Mandelstam variable u
        m_X: Mass of the electroweakino
        m_sq: Mass of the squark
    """
    return sympy.Eq(
        2 * sympy.re(M_s * sympy.conjugate(M_u)),
        g_s**2
        * C_A
        * C_F
        * B
        / (s * (u - m_sq**2))
        * (
            2 * (m_X**4 - m_sq**4)
            + m_sq**2 * (2 * u - 3 * s)
            - 2 * m_X**2 * (2 * m_sq**2 + u)
            - s * u
        ),
    )


@equation()
def equation_2_8(
    M=sympy.Symbol("M"),
    M_s=sympy.Symbol("M_s"),
    M_u=sympy.Symbol("M_u"),
):
    """
    total spin- and colour-averaged squared amplitude

    Args:
        M: Matrix element for the process
        M_s: Matrix element for the s channel
        M_u: Matrix element for the u channel
    """
    return sympy.Eq(
        sympy.Abs(M) ** 2,
        (
            sympy.Abs(M_s) ** 2
            + sympy.Abs(M_u) ** 2
            + 2 * sympy.re(M_s * sympy.conjugate(M_u))
        )
        / 96,
    )


@bib()
def bibtex():
    bibtex: str = """
@article{Fiaschi:2022odp,
    author = "Fiaschi, Juri and Fuks, Benjamin and Klasen, Michael and Neuwirth, Alexander",
    title = "{Soft gluon resummation for associated squark-electroweakino production at the LHC}",
    eprint = "2202.13416",
    archivePrefix = "arXiv",
    primaryClass = "hep-ph",
    reportNumber = "MS-TP-22-05, LTH 1299",
    doi = "10.1007/JHEP06(2022)130",
    journal = "JHEP",
    volume = "06",
    pages = "130",
    year = "2022"
}
"""
    return bibtex
