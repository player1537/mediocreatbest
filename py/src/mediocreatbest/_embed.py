"""
%%embed: Jupyter Magic to copy a function into the next cell
"""

from __future__ import annotations
from ._auto import auto


__all__ = [
    'embed',
]

try:
    get_ipython
except NameError:
    pass  # Not in Jupyter
else:
    @auto.IPython.core.magic.register_cell_magic('mediocreatbest.embed')
    @auto.IPython.core.magic.register_cell_magic('embed')
    @auto.IPython.core.magic.register_line_magic('mediocreatbest.embed')
    @auto.IPython.core.magic.register_line_magic('embed')
    def embed(line: str, cell: str=None):
        import inspect, textwrap

        def embed(arg: str, replace: bool):
            arg = get_ipython().ev(arg)
            arg = inspect.getsource(arg)
            arg = textwrap.dedent(arg)
            if replace:
                arg = f'# %mediocreatbest.embed {line}\n{arg}'
                get_ipython().set_next_input(arg, replace=replace)
            else:
                get_ipython().set_next_input(f'# %mediocreatbest.embed {line}\n{cell if cell is not None else ""}', replace=True)
                get_ipython().set_next_input(arg, replace=False)

        opt_replace = False

        arg = line.strip()
        if arg.startswith('--replace'):
            opt_replace = True
            arg = arg.removeprefix('--replace')
            arg = arg.strip()

        embed(arg, replace=opt_replace)
