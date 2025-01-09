"""
%%source: Jupyter Magic to source a shell script
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'source',
]


try:
    get_ipython
except NameError:
    pass
else:
    @auto.IPython.core.magic.register_line_magic('mediocreatbest.source')
    @auto.IPython.core.magic.register_line_magic('source')
    @auto.IPython.core.magic.register_cell_magic('mediocreatbest.source')
    @auto.IPython.core.magic.register_cell_magic('source')
    def source(magic_line, magic_cell=None):
        import os, subprocess, shlex

        if magic_cell is None or magic_cell == '':
            before = os.environ.copy()

            process = subprocess.run([
                'bash', '-c', f'source {magic_line}; export',
            ], capture_output=True, text=True)

            after = {}
            for line in process.stdout.split('\n'):
                if line == '': continue
                parts = shlex.split(line)
                assert parts[0] == 'declare', f'{line=!r}'
                assert parts[1] == '-x', f'{line=!r}'
                if '=' not in parts[2]: continue
                name, value = parts[2].split('=', 1)

                if before.get(name, None) == value: continue
                after[name] = value

            magic_cell = f'%%source {magic_line}\n'
            magic_cell += f'os.environ |= {{\n'
            for name, value in after.items():
                magic_cell += f'  {name!r}: '
                if ':' in value:
                    magic_cell += f'":".join([\n'
                    for value in value.split(':'):
                        magic_cell += f'    {value!r},\n'
                    magic_cell += f'  ]),\n'
                else:
                    magic_cell += f' {value!r},\n'
            magic_cell += f'}}\n'

            get_ipython().set_next_input(magic_cell, replace=True)

        get_ipython().run_cell(magic_cell)
