import sympy
from equation_database.util.doc import bib, equation
from equation_database.util.parse import frac


@equation()
def equation_2_1_30(
    sigma_0=sympy.Symbol("sigma_0"),
    alpha=sympy.Symbol("alpha"),
    e_q=sympy.Symbol("e_q"),
    Q=sympy.Symbol("Q"),
):
    """
    Cross section for $\\gamma^* \\to q \\bar q$

    Args:
        sigma_0: norm cross section
        alpha: fine structure constant
        e_q: electric charge of the quark
        Q: mass of the virtual photon
    """
    return sympy.Eq(sigma_0, 3 * alpha * e_q**2 * Q)


@equation()
def equation_2_3_32(
    sigma=sympy.Symbol("sigma"),
    sigma_0=sympy.Symbol("sigma_0"),
    alpha_s=sympy.Symbol("alpha_s"),
    x_1=sympy.Symbol("x_1"),
    x_2=sympy.Symbol("x_2"),
):
    """
    Differentiated cross section for $e^+e^- \\to q \\bar q g$

    Args:
        sigma: cross section
        sigma_0: norm cross section
        alpha_s: strong coupling constant
        x_1: quark momentum fraction
        x_2: antiquark momentum fraction
    """
    return sympy.Eq(
        sympy.Derivative(sigma, x_1, x_2) / sigma_0,
        2 * alpha_s / 3 / sympy.pi * (x_1**2 + x_2**2) / ((1 - x_1) * (1 - x_2)),
    )


@equation()
def equation_4_3_20(
    e=sympy.Symbol("e"),
    e_q=sympy.Symbol("e_q"),
    g_s=sympy.Symbol("g_s"),
    Q=sympy.Symbol("Q"),
    u=sympy.Symbol("u"),
    t=sympy.Symbol("t"),
):
    """
    $\\gamma^* g \\to q \\bar q$ scattering averaged matrix element

    Args:
        e: electric charge
        e_q: electric charge of the quark
        g_s: strong coupling constant
        Q: mass of the virtual photon
        u: Mandelstam variable u
        t: Mandelstam variable t

    """
    return (
        e**2
        * e_q**2
        * g_s**2
        * frac("4/8")
        * frac("1/2")
        * 8
        * (u / t + t / u + 2 * Q**2 * (u + t + Q**2) / (t * u))
    )


@bib()
def bibtex():
    # https://www.desy.de/~jung/qcd_and_mc_2009-2010/R.Field-Applications-of-pQCD.pdf
    return """
  @book{Field:1989uq,
      author = "Field, R. D.",
      title = "{Applications of Perturbative QCD}",
      volume = "77",
      year = "1989"
  }
  """
