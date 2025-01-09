"""
doctest: Run doctests on a single function
"""

from __future__ import annotations
from ._auto import auto


__all__ = [
    'doctest',
]


def doctest(func=None, /, verbose=False, sterile=False):
    def wrapper(func):
        # Thanks https://stackoverflow.com/a/49659927
        import doctest, copy

        # I need this to error out on failure; the default one doesn't.
        def run_docstring_examples(f, globs, verbose=False, name="NoName", compileflags=None, optionflags=0):
            finder = doctest.DocTestFinder(verbose=verbose, recurse=False)
            runner = doctest.DocTestRunner(verbose=verbose, optionflags=optionflags)
            for test in finder.find(func, name, globs=globs):
                runner.run(test, compileflags=compileflags)
            assert runner.failures == 0

        name = func.__name__

        if sterile:
            globs = {}
        else:
            globs = copy.copy(globals())
        globs[name] = func
        run_docstring_examples(func, globs, verbose=verbose, name=name)
        return func

    if func is not None:
        return wrapper(func)
    else:
        return wrapper
