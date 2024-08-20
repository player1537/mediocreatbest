"""
%%scope: Jupyter Magic: Lexical Scope Cell
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'scope',
]


try:
    get_ipython
except NameError:
    pass
else:
    @auto.IPython.core.magic.register_cell_magic('mediocreatbest.scope')
    @auto.IPython.core.magic.register_cell_magic('scope')
    def scope(line: str, cell: str):
        def scope(
            filename: str,
            name: str,
            inpvars: list[tuple[str, str]],
            outvars: list[tuple[str, str]],
            skip: bool,
            *,
            line=line,
            cell=cell,
        ):
            cell = get_ipython().transform_cell(
                cell,
            )

            module = auto.ast.parse(
                cell,
                filename,
                'exec',
            )

    #             auto.astpretty.pprint(module)

            kwonlyargs = []
            kw_defaults = []
            for inpvar, inpval in inpvars:
                kwonlyargs.append(auto.ast.arg(
                    arg=(
                        inpvar
                    ),
                    annotation=None,
                    type_comment=None,
                ))
                kw_defaults.append(None)

            value = None
            if len(outvars) == 0:
                value = auto.ast.Constant(
                    value=None,
                )

            elif len(outvars) == 1:
                value = auto.ast.Name(
                    id=(
                        outvars[0][0]
                    ),
                    ctx=auto.ast.Load(),
                )

            else:
                elts = []
                for outvar, outval in outvars:
                    elts.append(auto.ast.parse(
                        outval,
                        mode='eval',
                    ).body)

                tuple_ = auto.ast.Tuple(
                    elts=(
                        elts
                    ),
                    ctx=auto.ast.Load(),
                )

                value = tuple_

            return_ = auto.ast.Return(
                value=(
                    value
                ),
            )

            body = module.body[:]
            body.append(return_)

            function = auto.ast.FunctionDef(
                name=(
                    name
                ),
                args=auto.ast.arguments(
                    posonlyargs=[],
                    args=[],
                    vararg=None,
                    kwonlyargs=(
                        kwonlyargs
                    ),
                    kw_defaults=(
                        kw_defaults
                    ),
                    kwarg=None,
                    defaults=[],
                ),
                body=(
                    body
                ),
                decorator_list=[],
                returns=None,
                type_comment=None,
            )

            body = []
            body.append(function)

            if not skip:
                target = None

                if len(outvars) == 0:
                    target = auto.ast.Name(
                        id=(
                            '_'
                        ),
                        ctx=auto.ast.Store(),
                    )

                elif len(outvars) == 1:
                    target = auto.ast.Name(
                        id=(
                            outvars[0][0]
                        ),
                        ctx=auto.ast.Store(),
                    )

                else:
                    elts = []
                    for outvar, outval in outvars:
                        elts.append(auto.ast.Name(
                            id=(
                                outvar
                            ),
                            ctx=auto.ast.Store(),
                        ))

                    tuple_ = auto.ast.Tuple(
                        elts=(
                            elts
                        ),
                        ctx=auto.ast.Store(),
                    )

                    target = tuple_

                targets = []
                targets.append(target)

                keywords = []
                for inpvar, inpval in inpvars:
                    keywords.append(auto.ast.keyword(
                        arg=(
                            inpvar
                        ),
                        value=auto.ast.parse(
                            inpval,
                            mode='eval',
                        ).body,
                    ))

                call = auto.ast.Call(
                    func=auto.ast.Name(
                        id=(
                            name
                        ),
                        ctx=auto.ast.Load(),
                    ),
                    args=[],
                    keywords=(
                        keywords
                    ),
                    starargs=None,
                    kwargs=None,
                )

                assign = auto.ast.Assign(
                    targets=(
                        targets
                    ),
                    value=(
                        call
                    ),
                    type_comment=None,
                )

                body.append(assign)
            #/if not skip

            module = auto.ast.Module(
                body=(
                    body
                ),
                type_ignores=[],
            )

            module = auto.ast.fix_missing_locations(module)

            # pretty print ast tree
            # auto.astpretty.pprint(module)

            code = compile(module, filename, 'exec')
            get_ipython().ex(code)

            return module

        stack = auto.traceback.extract_stack()
        # print(f'{stack[-1].filename = !r}')
        # print(f'{stack[-2].filename = !r}')
        # print(f'{stack[-3].filename = !r}')
        # print(f'{stack[-4].filename = !r}')
        # print(f'{stack[-5].filename = !r}')
        # print(f'{stack[-6].filename = !r}')
        filename = stack[-4].filename

        def csv(s: str) -> list[str]:
            return s.split(',')

        def kv(s: str, /) -> tuple[str, str]:
            kv = s.split('=', 1)
            if len(kv) == 1:
                return kv[0], kv[0]
            else:
                k, v = kv
                return k, v

        parser = auto.argparse.ArgumentParser()
        parser.add_argument('--name', '-n', default='scope')
        parser.add_argument('--inpvars', '-i', type=kv, default=[], action='append')
        parser.add_argument('--outvars', '-o', type=kv, default=[], action='append')
        parser.add_argument('--skip', action='store_true')

        args = auto.shlex.split(line)
        args = vars(parser.parse_args(args))

        scope(filename=filename, **args)
