"""

"""

from __future__ import annotations
from ._auto import auto


@auto.contextlib.contextmanager
def track(
    path: auto.pathlib.Path,
    *args,
    **kwargs,
) -> auto.typing.IO:
    with auto.contextlib.ExitStack() as stack:
        pbar = stack.enter_context( auto.tqdm.auto.tqdm(
            unit='B',
            unit_scale=True,
        ) )
        pbar.reset(total=(
            path.stat().st_size
        ) if path.exists() else (
            None
        ))

        f = stack.enter_context( path.open(*args, **kwargs) )

        def scope():
            while not ev.is_set():
                auto.time.sleep(0.1)

                n = f.tell()
                pbar.update(n - pbar.n)

        t = auto.threading.Thread(target=scope)
        # t.daemon = True
        stack.callback( t.join )

        ev = auto.threading.Event()
        stack.callback( ev.set )

        t.start()

        yield f
