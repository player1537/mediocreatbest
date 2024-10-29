"""

"""

from __future__ import annotations
from ._auto import auto


def SQLQuery(s: str, /, **kwargs):
    environment = auto.jinja2.Environment()
    environment.filters['tosqlref'] = lambda x: '"' + str(x).replace('"', '""') + '"'
    environment.filters['tosqlstr'] = lambda x: "'" + str(x).replace("'", "''") + "'"
    environment.filters['tosqlint'] = lambda x: str(int(str(x)))
    environment.globals['auto'] = auto

    template = environment.from_string(s)

    return template.render(**kwargs)


def SQLQuery_verbose(s: str, /, **kwargs):
    s = SQLQuery(s, **kwargs)

    with auto.mediocreatbest.Textarea():
        print(s)

    return s

SQLQuery.verbose = SQLQuery_verbose
