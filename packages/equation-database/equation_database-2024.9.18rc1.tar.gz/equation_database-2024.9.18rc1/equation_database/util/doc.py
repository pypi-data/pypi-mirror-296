import sympy


def equation():
    """

    Args:
        path: The path of the file to wrap
        field_storage: The :class:`FileStorage` instance to wrap
        temporary: Whether or not to delete the file when the File
           instance is destructed

    Returns:
        BufferedFileStorage: A buffered writable file descriptor

    """

    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        r = target()
        # if array loop
        tex = ""
        if isinstance(r, tuple):
            tex = tex + "\n\n    Returns:"
            for i in r:
                tex = tex + "\n        $" + sympy.latex(i) + "$,"
            tex = tex + "\n\n    Example:"
            for n, i in enumerate(r):
                tex += (
                    "\n"
                    + indent_string_twice(
                        f">>> print(sympy.latex({target.__name__}()[{n}]))"
                    )
                    + "\n"
                    + indent_string_twice(sympy.latex(i))
                )
                # tex += indent_string_twice(f">>> print(sympy.mathml({target.__name__}()))") + "\n" + indent_string_twice(sympy.mathml(r))
        else:
            tex = tex + "\n\n    Returns:\n        $" + sympy.latex(r) + "$"
            tex = tex + "\n\n    Example:"
            tex += (
                "\n"
                + indent_string_twice(f">>> print(sympy.latex({target.__name__}()))")
                + "\n"
                + indent_string_twice(sympy.latex(r))
            )
            tex += (
                "\n"
                + indent_string_twice(f">>> print(sympy.mathml({target.__name__}()))")
                + "\n"
                + indent_string_twice(sympy.mathml(r))
            )
        target.__doc__ = target.__doc__ + tex
        return target

    return wrapper


def indent_string_twice(string):
    indented_string = "\n".join("        " + line for line in string.splitlines())
    return indented_string


def bib():
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        r = target()
        ret = target.__doc__
        try:
            import bibtexparser

            for entry in bibtexparser.loads(r).entries:
                if entry.get("doi"):
                    ret += f"`DOI <https://doi.org/{entry['doi']}>`_ "
                if entry.get("eprint"):
                    ret += f"`arXiv <https://arxiv.org/abs/{entry['eprint']}>`_ "
                if entry.get("url"):
                    ret += f"`URL <{entry['url']}>`_ "
                if entry.get("title"):
                    t = f"{entry['title']}"
                    if t[0] == "{" and t[-1] == "}":
                        t = t[1:-1]
                    ret += t + " "
        except ImportError:
            pass
        ret += "\n:: \n" + indent_string_twice(r)
        target.__doc__ = ret
        return target

    return wrapper


def table():
    def wrapper(target):
        if target.__doc__ is None:
            target.__doc__ = ""
        r = target()
        # Loop through the table and add only the second column (the LaTeX expression) to the docstring
        for key, expression in r.items():
            latex_expr = sympy.latex(expression)
            target.__doc__ += (
                f"\n\n- {key}:\n\n    ${latex_expr}$"  # TODO latex expression?
            )

        return target

    return wrapper
