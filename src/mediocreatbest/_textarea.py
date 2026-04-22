"""
Textarea context manager
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'Textarea',
]


class Textarea:
    def __init__(self, value: str | None = None, /):
        self.io = auto.io.StringIO()
        if value is not None:
            self.io.write(value)

    def _repr_html_(self):
        return f'<textarea rows=12 style="width: 90%; margin-left: 5%">{auto.html.escape(self.value)}</textarea>'

    def __enter__(self):
        self.stack = auto.contextlib.ExitStack()
        self.stack.enter_context( auto.contextlib.redirect_stdout(self.io) )
        return self

    def __exit__(self, *args):
        self.stack.close()
        self.value = self.io.getvalue()
        display(self)

def scope():
    with Textarea():
        print('hello')

# /scope
