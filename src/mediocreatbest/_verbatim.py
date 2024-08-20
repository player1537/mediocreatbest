"""
%%verbatim: Jupyter Magic: Assign verbatim contents of a cell as a local variable
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'verbatim',
]


try:
    get_ipython
except NameError:
    pass
else:
    @auto.IPython.core.magic.register_cell_magic('mediocreatbest.verbatim')
    @auto.IPython.core.magic.register_cell_magic('verbatim')
    def verbatim(line, cell=None):
        def verbatim(*, variable: str):
            get_ipython().push({
                variable: cell,
            })

        parser = auto.argparse.ArgumentParser()
        parser.add_argument('-v', dest='variable', default='verbvatim')
        args = vars(parser.parse_args(auto.shlex.split(line)))

        return verbatim(**args)
