"""
Tkinter Grid
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'Grid',
]


def Grid(parent: auto.tk.Widget, widgets: list[list[auto.tk.Widget]], /) -> None:
    nrows = len(widgets)
    assert nrows >= 1
    ncols = len(widgets[0])
    assert ncols >= 1
    for row in widgets:
        assert len(row) == ncols

    grid = {
        (ri, ci): widgets[ri][ci]
        for ri in range(nrows)
        for ci in range(ncols)
    }

    for ri in range(nrows):
        parent.grid_rowconfigure(ri, weight=1)

    for ci in range(ncols):
        parent.grid_columnconfigure(ci, weight=1)

    seen = set()
    for ri, ci in auto.itertools.product(range(nrows), range(ncols)):
        if id(grid[ri, ci]) in seen:
            continue
        seen.add(id(grid[ri, ci]))

        ri0, ci0 = ri, ci

        # Walk down
        for ri in range(ri0, nrows+1):
            if grid.get((ri, ci0), None) is not grid[ri0, ci0]:
                break

        # Walk right
        for ci in range(ci0, ncols+1):
            if grid.get((ri0, ci), None) is not grid[ri0, ci0]:
                break

        nr = ri - ri0
        nc = ci - ci0

        grid[ri0, ci0].grid(row=ri0, column=ci0, rowspan=nr, columnspan=nc, sticky='nsew')
