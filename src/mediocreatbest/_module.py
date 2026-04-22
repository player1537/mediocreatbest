"""
module: Jupyter Magic to define a module in a cell
"""

from __future__ import annotations
from ._auto import auto


__all__ = [
    'module',
]


try:
    get_ipython
except NameError:
    pass  # Not in Jupyter
else:
    @auto.IPython.core.magic.register_cell_magic('mediocreatbest.module')
    @auto.IPython.core.magic.register_cell_magic('module')
    def _(line: str, cell: str):
        __tracebackhide__ = True

        parser = auto.argparse.ArgumentParser()
        parser.add_argument('name', type=str)
        parser.add_argument('--reuse', action='store_true')
        args = parser.parse_args(auto.shlex.split(line))

        traceback = auto.traceback.extract_stack()
        filename = traceback[-4][0]

        code = get_ipython().transform_cell(cell)
        code = compile(code, filename, 'exec')

        if args.reuse and args.name in auto.sys.modules:
            module = auto.sys.modules[args.name]
        else:
            module = auto.types.ModuleType(args.name)

        try:
            exec(code, module.__dict__)
        except Exception as e:
            traceback = auto.traceback.extract_tb(auto.sys.exc_info()[2])
            frame = traceback[1]
            lineno = frame.lineno

            traceback = auto.traceback.format_exc()
            traceback = traceback.replace('<module>', f'<cell line: {lineno}>()')
            print(traceback)

            raise e from None

        auto.sys.modules[args.name] = module
        if hasattr(auto, args.name):
            delattr(auto, args.name)

        varname = args.name.split('.', 1)[0]
        get_ipython().push({
            varname: module,
        })

