"""

"""
from __future__ import annotations
from ._auto import auto
from ._config import config
from ._contextgenerator import contextgenerator
from ._doctest import doctest
from . import _embed
from ._getkey import getkey
from ._grid import Grid
from . import _module
from ._random import RANDOM
from ._run import run
from . import _scope
from ._singledispatch import dispatch
from . import _source
from ._sqlquery import SQLQuery
from ._stuple import stuple
from ._textarea import Textarea
from ._track import track
from . import _verbatim
from ._wrap import wrap



__all__ = [
    'auto',
]


#--- Auto Import Submodules

def __getattr__(name: str):
    if name.startswith('_') or name.endswith('_'):
        raise AttributeError(name)

    ckey = f'mediocreatbest.{name}'
    if ckey == 'mediocreatbest.lib':
        return auto.sys.modules['mediocreatbest']

    if ckey in auto.sys.modules:
        module = auto.sys.modules[ckey]
        return module

    raise AttributeError(name)



#--- DotDict: Access Dictionary Members with getattr

class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


#--- Convert HTML into a static https://itty.bitty.site link

def IttyBittySite(html: str, /) -> str:
    ret = html
    ret = bytes(ret, encoding="utf-8")
    ret = auto.lzma.compress(ret, format=auto.lzma.FORMAT_ALONE, preset=9)
    ret = auto.base64.b64encode(ret)
    ret = ret.decode("utf-8")
    ret = 'https://itty.bitty.site/#/'+ret
    return ret


#--- Format Chat

def FormatChat(*, prompt: dict={}, output: None | dict=None, **kwargs) -> auto.IPython.display.HTML:
    prompt = prompt | kwargs
    ret = r"""
        <script src="https://cdn.tailwindcss.com"></script>
        <div class="
            flex
            flex-col
            w-[640px]
            border
        ">
        {% for message in messages %}
            <div
                class="
                    w-[80%]
                    p-4
                    m-2
                    rounded-lg
                    whitespace-pre-wrap
                    text-left
                    {% if message.role == 'system' %}
                    self-center
                    bg-gray-100
                    {% elif message.role == 'user' %}
                    self-end
                    bg-blue-100
                    {% elif message.role == 'assistant' %}
                    self-start
                    bg-gray-100
                    {% endif %}
                "
            >{{ message.content | replace("\n", "⏎\n") | escape }}</div>
        {% endfor %}
        </div>
    """

    ret = auto.textwrap.dedent(ret)
    ret = auto.jinja2.Template(ret)
    ret = ret.render(
        messages=(
            [*prompt['messages'], output['choices'][0]['message']]
            if output is not None else
            prompt['messages']
        ),
    )
    url = IttyBittySite(ret)
    ret = (
        f'''<a href="{url}" class="underline text-blue-500">[itty bitty site]</a>'''
    ) + ret
    ret = auto.IPython.display.HTML(ret)
    return ret


#--- Hide the contents of the string when printed in repr format

class HiddenStr(auto.collections.UserString):
    def __repr__(self):
        return f'<{self.__class__.__name__}>'


#--- TEMPLATE

#@title TEMPLATE { display-mode: "form" }
#@markdown ```python
#@markdown TEMPLATE = (
#@markdown     s: str,
#@markdown     /,
#@markdown ) -> Template
#@markdown ```
#@markdown ```python
#@markdown TEMPLATE = (
#@markdown     s: str,
#@markdown     /,
#@markdown     **context: dict,
#@markdown ) -> str
#@markdown ```
#@markdown ```python
#@markdown Template = (
#@markdown     **context: dict,
#@markdown ) -> str
#@markdown ```

def TEMPLATE(s: str, /, **context):
    env = auto.jinja2.Environment(
    )
    env.globals.update({
        'auto': auto,
    })

    template = env.from_string(s)

    def Template(**context):
        return template.render(**context)

    if not context:
        return Template
    else:
        return Template(**context)


#--- Export

#@title Export { display-mode: "form" }
#@markdown ```python
#@markdown with Export(
#@markdown     name: str,
#@markdown     /,
#@markdown     mode: auto.typing.Literal['w'] = 'wb',
#@markdown ) -> typing.BinaryIO:
#@markdown     ...
#@markdown ```
#@markdown ```python
#@markdown with Export(
#@markdown     name: str,
#@markdown     /,
#@markdown     mode: auto.typing.Literal['w'] = 'wb',
#@markdown ) -> typing.TextIO:
#@markdown     ...
#@markdown ```
#@markdown ```python
#@markdown Export.clear = (
#@markdown ) -> None
#@markdown ```

@auto.contextlib.contextmanager
def Export(
    name: str,
    /,
    mode: auto.typing.Literal['w', 'wb'] = 'wb',
):
    assert mode in ['w', 'wb']

    path = Export.path
    if path.exists():
        old_size = path.stat().st_size
    else:
        old_size = None

    if path.exists():
        to_delete = []
        with auto.zipfile.ZipFile(path, 'r') as arc:
            names = arc.namelist()
            if name in names:
                to_delete.append(name)

        if to_delete:
            auto.subprocess.run([
                'zip',
                '-d',
                path,
                *to_delete,
            ])

    with auto.contextlib.ExitStack() as stack:
        arc = stack.enter_context(auto.zipfile.ZipFile(path, 'a'))

        f = stack.enter_context(arc.open(name, 'w'))
        if mode == 'w':
            f = stack.enter_context(auto.io.TextIOWrapper(f))
        elif mode == 'wb':
            pass
        else:
            raise ValueError(f'{mode=}')

        yield f

    new_size = path.stat().st_size
    if old_size is not None:
        print(f'Added {new_size-old_size:,d} bytes to {path}')
        print(f'  Total: {new_size:,d} bytes')
    else:
        print(f'Wrote {new_size:,d} bytes to {path}')

def __Export_clear():
    if Export.path.exists():
        Export.path.unlink()

Export.path = auto.pathlib.Path('export.zip')
Export.clear = __Export_clear
# /Export.clear


#--- Grow

#@title Grow { display-mode: "form" }
#@markdown ```python
#@markdown # +/- d
#@markdown Grow = (
#@markdown     lo,
#@markdown     hi,
#@markdown     /,
#@markdown     *,
#@markdown     d: float,
#@markdown ) -> tuple[float, float]
#@markdown ```
#@markdown ```python
#@markdown # +/- p * (hi - lo)
#@markdown Grow = (
#@markdown     lo,
#@markdown     hi,
#@markdown     /,
#@markdown     *,
#@markdown     p: float,
#@markdown ) -> tuple[float, float]
#@markdown ```

def Grow(lo, hi, /, *, d=None, p=None):
    assert (d is not None) != (p is not None)
    if p is not None:
        mi = (lo + hi) / 2
        newlo, newhi = (
            mi - (hi - lo)/2 * (1.0 + p),
            mi + (hi - lo)/2 * (1.0 + p),
        )
    elif d is not None:
        newlo, newhi = (
            lo - d,
            hi + d,
        )
    else:
        raise NotImplementedError()

    eps = 1e-3
    assert newlo <= lo + eps, \
        f'{newlo=!r} !<= {lo=!r}'
    assert newhi >= hi - eps, \
        f'{newhi=!r} !>= {hi=!r}'

    # print(f'Grow [{lo}, {hi}] to [{newlo}, {newhi}] ({d=}, {p=})')
    return newlo, newhi


#--- Complete

# @title Complete { display-mode: "form" }
#@markdown ```python
#@markdown def Complete(
#@markdown     *,
#@markdown     config = Complete.config,
#@markdown     **prompt,
#@markdown ) -> dict:
#@markdown     ...
#@markdown ```

def Complete(
    *,
    config=None,
    block = True,
    **prompt,
):
    if config is None:
        config = Complete.config

    prompt.setdefault('model', config.model)

    key = auto.json.dumps(prompt, sort_keys=True)
    key = auto.hashlib.sha256(key.encode()).hexdigest()
    if key not in Complete.cache:
        if not block:
            with Complete.lock:
                with open(Complete.todo, 'a') as f:
                    auto.json.dump({ key: prompt }, f)

            return None

        url = config.base_url
        if 'prompt' in prompt:
            url = auto.urllib.parse.urljoin(url,
                'completion',
            )

        elif 'messages' in prompt:
            url = auto.urllib.parse.urljoin(url,
                'v1/chat/completions',
            )

        else:
            assert False

        with auto.requests.request(
            'POST',
            url,
            headers={
                'Accept': 'application/json',
                'Authorization': f'Bearer {config.api_key}',
                'Content-Type': 'application/json',
            },
            json=prompt,
        ) as r:
            r.raise_for_status()
            output = r.json()

        Complete.was_cached = False
        Complete.cache[key] = output

    else:
        Complete.was_cached = True
        output = Complete.cache[key]

    return output

try:
    __Complete_cache
except NameError:
    __Complete_cache = {}
# __Complete_cache.clear()

Complete.cache = __Complete_cache
# Complete.config = config.complete.default
Complete.lock = auto.threading.Lock()
Complete.todo = auto.pathlib.Path('complete.todo.ndjson')

def scope():
    auto.pprint.pp(Complete(
        messages=[
            { 'role': 'user', 'content': 'What is the capital of France?' },
        ],
        max_tokens=100,
        # config=config.complete.tinyllama,
        block=False,
    ))

# /scope


#--- PROMPT

#@title PROMPT { display-mode: "form" }

#@markdown ```python
#@markdown def PROMPT(
#@markdown     s: str,
#@markdown     /,
#@markdown ) -> Prompt:
#@markdown     ...
#@markdown
#@markdown def Prompt(
#@markdown     **query,
#@markdown ) -> dict:
#@markdown     ...
#@markdown ```

@auto.functools.cache
def PROMPT(s: str, /):
    def Prompt(**query):
        environment = auto.jinja2.Environment(
            loader=auto.jinja2.DictLoader(PROMPT.templates),
            undefined=auto.jinja2.StrictUndefined,
        )
        environment.globals.update({
            'auto': auto,
        })
        template = environment.from_string(s)

        _messages = None
        def AddMessage(role: str, content: str):
            nonlocal _messages
            if _messages is None:
                _messages = []
            content = content.strip()
            _messages.append(dict(
                role=role,
                content=content,
            ))
            return f'<Message({role!r}, {content!r})>'
        environment.globals |= dict(
            user=lambda caller: AddMessage('user', caller()),
            assistant=lambda caller: AddMessage('assistant', caller()),
            system=lambda caller: AddMessage('system', caller()),
        )

        _prompt = None
        def SetPrompt(prompt: str):
            nonlocal _prompt
            _prompt = prompt
            return f'<Prompt({prompt!r})>'
        environment.globals |= dict(
            prompt=lambda caller: SetPrompt(caller()),
        )

        _grammar = None
        def SetGrammar(grammar: str):
            nonlocal _grammar
            _grammar = grammar
            return f'<Grammar({grammar!r})>'
        environment.globals |= dict(
            grammar=lambda caller: SetGrammar(caller()),
        )

        _parser = None
        def SetParser(parser: str):
            nonlocal _parser
            _parser = parser
            return f'<Parser({parser!r})>'
        environment.globals |= dict(
            parser=lambda caller: SetParser(caller()),
        )

        context = {}
        context |= query

        _ = template.render(
            **context,
        )

        prompt = auto.collections.UserDict(
        )

        assert (bool(_messages) != bool(_prompt)), \
            f"Exactly one of 'messages' or 'prompt' must be specified."
        if _messages is not None:
            prompt |= dict(
                messages=_messages,
            )
        elif _prompt is not None:
            prompt |= dict(
                prompt=_prompt,
            )
        else:
            assert False

        if _grammar is not None:
            prompt |= dict(
                grammar=_grammar,
            )

        if _parser is not None:
            prompt.parser = _parser
        return prompt

    return Prompt

PROMPT.templates = {}

def scope():
    PROMPT.templates['capital'] = r"""
    {% macro capital(where) -%}
    {% call system() %}
    You are a helpful AI assistant.
    {% endcall %}

    {% call user() %}
    What is the capital of {{ where }}?
    {% endcall %}
    {% endmacro %}
    """

    display(auto.mediocreatbest.FormatChat(
        prompt=PROMPT(r"""
    {% from 'capital' import capital %}
    {{ capital("France") }}

    {% call grammar() %}
    root ::= intro
    intro ::= "The capital of {{ where }} is " quoted
    quoted ::= "\"" [^"]+ "\""
    {% endcall %}

    {% call parser() %}
    "(?P<quoted>[^"]+)"
    {% endcall %}
    """)(
        where='France',
    )))

# /scope


def scope():
    messages = [
        {
            'role': 'user',
            'content': 'What is the capital of France?',
        },
        {
            'role': 'assistant',
            'content': 'Paris',
        },
        {
            'role': 'user',
            'content': 'What is the capital of Germany?',
        },
        {
            'role': 'assistant',
            'content': None,
        },
    ]
#     /auto.pprint.pp messages width=144

    prompt = ChatML(messages)
#     /auto.pprint.pp prompt width=144

# /scope


#--- Embed

#@title Embed { display-mode: "form" }
#@markdown ```python
#@markdown def Embed(
#@markdown     *,
#@markdown     query: str | list[str] | None = None,
#@markdown     passage: str | list[str] | None = None,
#@markdown     batch: int | None = None,
#@markdown     progress: None | auto.typing.Any = None,
#@markdown ) -> auto.np.ndarray[float]:
#@markdown     ...
#@markdown ```

def Embed(
    *,
    query: str | list[str] | None = None,
    passage: str | list[str] | None = None,
    batch: int | None = None,
    progress: None | auto.typing.Any = None,
    config: auto.typing.Any | None = None,
) -> auto.np.ndarray[float]:
    def Batch(seq, /, *, batch: int | None) -> auto.typing.Iterable[list]:
        if batch is None:
            yield seq
            return

        for i in range(0, len(seq), batch):
            yield seq[i:i+batch]

    assert (query is not None) != (passage is not None), \
        f"Exactly one of 'query' or 'passage' must be specified."

    if config is None:
        config = Embed.config

    inputs = []
    if query is not None:
        if isinstance(query, str):
            query = [query]
        inputs = [
            f'query: {q}'
            for q in query
        ]

    elif passage is not None:
        if isinstance(passage, str):
            passage = [passage]
        inputs = [
            f'passage: {p}'
            for p in passage
        ]

    needs = []
    for input in inputs:
        key = auto.hashlib.sha256(input.encode()).hexdigest()
        if key not in Embed.cache:
            needs.append(input)

    if needs:
        if progress is not None:
            progress.reset(len(needs))

        for needs in Batch(needs, batch=batch):
            with auto.requests.request(
                'POST',
                f'{config.base_url}embeddings',
                headers={
                    'Accept': 'application/json',
                    'Authorization': f'Bearer {config.api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'input': needs,
                },
            ) as r:
                r.raise_for_status()
                output = r.json()

            if progress is not None:
                progress.update(len(needs))

            for input, data in zip(needs, output['data']):
                embed = data['embedding']
                key = auto.hashlib.sha256(input.encode()).hexdigest()
                Embed.cache[key] = embed

    embeds = []
    for input in inputs:
        key = auto.hashlib.sha256(input.encode()).hexdigest()
        assert key in Embed.cache
        embeds.append(Embed.cache[key])

    embeds = auto.np.stack(embeds, axis=0)

    if len(embeds) == 1:
        return embeds[0]
    return embeds

Embed.cache = {}
# Embed.config = config.embed.default

def scope():
    display(Embed(
        query='What is the capital of France?',
    )[:10])

    display(auto.np.dot(
        Embed(
            query='What is the capital of France?',
        ),
        Embed(
            passage='Paris is the capital of France.',
        ),
    ))

# /scope


#--- Enlookup

#@title Enlookup { display-mode: "form" }
#@markdown ```python
#@markdown class Enlookup:
#@markdown     ...
#@markdown ```

class Enlookup(auto.collections.UserList):
    def __init__(self, *args, key=str, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except (KeyError, TypeError):
            pass

        for d in self.data:
            if self.key(d) == key:
                return d

        if isinstance(key, list):
            return Enlookup([self[k] for k in key])

        if isinstance(key, tuple):
            key, offset = key
        else:
            offset = 0

        embeds = Embed(
            passage=list(map(self.key, self.data)),
            batch=1_000,
        )

        embed = Embed(
            query=str(key),
        )

        cdist = auto.scipy.spatial.distance.cdist(
            embeds,
            [embed],
            metric='cosine',
        )
        assert len(cdist.shape) == 2, \
            f'{cdist.shape=} is not length 2'
        assert cdist.shape[1] == 1, \
            f'{cdist.shape[1]=} is not 1'
        cdist = cdist[:, 0]
        assert len(cdist.shape) == 1, \
            f'{cdist.shape=} is not length 1'

        inds = auto.numpy.argsort(cdist)
        ind = inds[offset]

        return self.data[ind]

def scope():
    lookup = Enlookup('''Social Vulnerability - Score
Prevention: Health Insurance: Current lack of health insurance among adults aged 18-64 years
tot_park_area_sqmiles'''.split('\n'))

    for k in ['risk', 'prevention', 'park area']:
        auto.pprint.pp({ k: lookup[k] })
        auto.pprint.pp({ (k, 1): lookup[k, 1] })

    auto.pprint.pp(lookup[['risk', 'prevention', 'park area']])
    auto.pprint.pp(lookup[[('risk', 1), ('prevention', 1), ('park area', 1)]])

# /scope


#--- Clipboard

#@title Clipboard
def Clipboard(
    d: dict[str, str] = {},
    /,
    *,
    ipynb: None | str | list[str] = None,
) -> auto.IPython.display.HTML:
    if ipynb is not None:
        if isinstance(ipynb, str):
            ipynb = [ipynb]

        # d['text/plain'] = ipynb
        d['application/ipynb'] = auto.json.dumps([
            {
                'cell_type': 'code',
                'metadata': {},
                'execution_count': None,
                'source': ipynb.splitlines(keepends=True),
                'outputs': [],
            }
            for ipynb in ipynb
        ])

    js = auto.google.colab.syntax.javascript(TEMPLATE(r"""
        (() => {
            clipboard.write([
                {%- for k, v in d.items() %}
                (() => {
                    const t = {{ auto.json.dumps(k) | safe }};
                    const v = {{ auto.json.dumps(v) | safe }};
                    const b = new Blob([v], { type: t });
                    const c = new clipboard.ClipboardItem({ [t]: b });
                    return c;
                })(),
                {%- endfor %}
            ]);
        })();
    """, **locals()))

    html = auto.google.colab.syntax.html(TEMPLATE(r"""
        <script src="https://unpkg.com/clipboard-polyfill@4.0.2/dist/es5/window-var/clipboard-polyfill.window-var.es5.js"></script>
        <button onclick="javascript:{{ js | escape }}">Copy</button>
    """, **locals()))

    html = auto.IPython.display.HTML(html)
    return html

def scope():
    display(Clipboard({
        'text/plain': 'Hello, world!',
    }))

    display(Clipboard(ipynb=r"""
def scope():
    print("Hello, world!")

/scope
"""))

# /scope


def with_exit_stack(func, /):
    signature = auto.inspect.signature(func)

    @auto.functools.wraps(func)
    def wrapper(*args, **kwargs):
        with auto.contextlib.ExitStack() as stack:
            if 'stack' in signature.parameters:
                kwargs = kwargs | dict(stack=stack)
            if 'enter' in signature.parameters:
                kwargs = kwargs | dict(enter=stack.enter_context)
            if 'defer' in signature.parameters:
                kwargs = kwargs | dict(defer=stack.callback)

            return func(*args, **kwargs)

    return wrapper


def summary(
    df,
    /,
) -> str:
    df = df.sample(3, random_state=1337)

    df = df.T

    with auto.warnings.catch_warnings():
        auto.warnings.simplefilter('ignore', FutureWarning)

        df = df.applymap(str)
        df = df.applymap(lambda s: auto.textwrap.shorten(s, 72//2))

    return df.to_markdown()


@with_exit_stack
def encrypt(
    *,   enter,

    dec_path: auto.os.PathLike,

    password: str | auto.typing.Literal[...] = ...,
    password_name: str | None = None,

    verbose: bool = True,

    enc_path: auto.os.PathLike | auto.typing.Literal[...] = ...,
    enc_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    enc_name: str | auto.typing.Literal[...] = ...,

    tmp_path: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_name: str = 'encrypt.tmp',
) -> auto.pathlib.Path:
    dec_path = auto.pathlib.Path(dec_path)

    if enc_path is ...:
        if enc_root is ...:
            enc_root = dec_path.parent
        if enc_name is ...:
            enc_name = f'{dec_path.name}.enc'
        enc_path = enc_root / enc_name
    else:
        enc_path = auto.pathlib.Path(enc_path)

    if password is ...:
        global __94dc6d48
        try: __94dc6d48
        except NameError: __94dc6d48 = auto.functools.cache(auto.google.colab.userdata.get)
        password = __94dc6d48(password_name)
    assert password is not None

    if tmp_path is ...:
        if tmp_root is ...:
            tmp_root = enc_path.parent
        tmp_path = tmp_root / tmp_name

    if verbose:
        pbar = enter( auto.tqdm.auto.tqdm(
            total=int(dec_path.stat().st_size),
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc='Encrypt',
        ) )

    p = enter( auto.subprocess.Popen([
        'openssl', 'enc',
        '-aes-256-ctr',
        '-pbkdf2',
        '-md', 'sha-256',
        # '-in', enc_path,
        '-out', tmp_path,
        '-pass', f'pass:{password}',
    ], stdin=auto.subprocess.PIPE) )

    with dec_path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            if verbose:
                pbar.update(len(chunk))

            p.stdin.write(chunk)

    p.stdin.close()
    p.wait()
    assert p.returncode == 0, p.returncode

    tmp_path.rename(enc_path)
    assert enc_path.exists(), enc_path

    return enc_path


@with_exit_stack
def decrypt(
    *,   enter,
    verbose: bool = True,

    enc_path: auto.os.PathLike,

    password: str | auto.typing.Literal[...] = ...,
    password_name: str | None = None,

    dec_path: auto.os.PathLike,
    dec_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    dec_name: str | auto.typing.Literal[...] = ...,

    tmp_path: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_name: str = 'decrypt.tmp',
) -> auto.pathlib.Path:
    enc_path = auto.pathlib.Path(enc_path)

    if dec_path is ...:
        if dec_root is ...:
            dec_root = enc_path.parent
        if dec_name is ...:
            dec_name = enc_path.name.removesuffix('.enc')
        dec_path = dec_root / dec_name
    else:
        dec_path = auto.pathlib.Path(dec_path)

    if password is ...:
        global __94dc6d48
        try: __94dc6d48
        except NameError: __94dc6d48 = auto.functools.cache(auto.google.colab.userdata.get)
        password = __94dc6d48(password_name)
    assert password is not None

    if tmp_path is ...:
        if tmp_root is ...:
            tmp_root = dec_path.parent
        tmp_path = tmp_root / tmp_name

    if verbose:
        pbar = enter( auto.tqdm.auto.tqdm(
            total=int(enc_path.stat().st_size),
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc='Decrypt',
        ) )

    p = enter( auto.subprocess.Popen([
        'openssl', 'enc',
        '-d',
        '-aes-256-ctr',
        '-pbkdf2',
        '-md', 'sha-256',
        '-out', tmp_path,
        '-pass', f'pass:{password}',
    ], stdin=auto.subprocess.PIPE) )

    with enc_path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            if verbose:
                pbar.update(len(chunk))

            p.stdin.write(chunk)

    p.stdin.close()
    p.wait()
    assert p.returncode == 0, p.returncode

    tmp_path.rename(dec_path)
    assert dec_path.exists(), dec_path

    return dec_path


@with_exit_stack
def download(
    *,   enter,
    path: auto.pathlib.Path | str = None,
    href: str = None,

    verbose: bool = True,

    tmp_path: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_root: auto.pathlib.Path | auto.typing.Literal[...] = ...,
    tmp_name: str = 'download.tmp',
) -> auto.pathlib.Path:
    if isinstance(path, str):
        path = auto.pathlib.Path(path)

    if tmp_path is ...:
        if tmp_root is ...:
            tmp_root = path.parent
        tmp_path = tmp_root / tmp_name

    r = enter( auto.requests.request(
        'GET',
        href,
        stream=True,
    ) )
    r.raise_for_status()

    if verbose:
        pbar = enter( auto.tqdm.auto.tqdm(
            total=int(r.headers.get('Content-Length', 0)),
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc='Download',
        ) )

    with tmp_path.open('wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if verbose:
                pbar.update(len(chunk))

            f.write(chunk)

    tmp_path.rename(path)
    assert path.exists(), path

    return path


@with_exit_stack
def checksum(
    *,   enter,
    path: auto.pathlib.Path | None = None,
    hash: str | auto.typing.Literal[...] | None = None,

    verbose: bool = True,
):
    if not hasattr(path, 'open'):
        path = auto.pathlib.Path(path)

    pbar = enter( auto.tqdm.auto.tqdm(
        leave=False,
        total=int(path.stat().st_size),
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc='Checksum',
    ) )

    h = auto.hashlib.new('sha256')
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            if verbose:
                pbar.update(len(chunk))

            h.update(chunk)

    h = h.hexdigest()
    assert h == hash, f'Invalid checksum: {h!r}'


def with_random(
    *,
    seed: int | None = None,
):
    def wrapper(func, /):
        @auto.functools.wraps(func)
        def inner(
            *args,
            seed = seed,
            Random: auto.mediocreatbest.RANDOM | auto.typing.Literal[...] = ...,
            **kwargs,
        ):
            if Random is ...:
                Random = auto.mediocreatbest.RANDOM(seed=seed)
            kwargs = kwargs | dict(Random=Random)

            ret = func(*args, **kwargs)

            return ret

        return inner

    return wrapper



@with_exit_stack
def checksum(
    *,   enter,
    path: auto.pathlib.Path | None = None,
    hash: str | auto.typing.Literal[...] | None = None,

    verbose: bool = True,
):
    if hash is None:
        return

    if not hasattr(path, 'open'):
        path = auto.pathlib.Path(path)

    pbar = enter( auto.tqdm.auto.tqdm(
        leave=False,
        total=int(path.stat().st_size),
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc='Checksum',
    ) )

    h = auto.hashlib.new('sha256')
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            if verbose:
                pbar.update(len(chunk))

            h.update(chunk)

    h = h.hexdigest()
    if hash is not Ellipsis:
        assert h == hash, f'Invalid checksum: {h!r}'
    else:
        print(f'Checksum: {h!r}')



@with_exit_stack
def terminal(
    args: str | list,
    *,   enter,
    verbose: bool = True,
) -> None:
    tmpdir = enter( auto.tempfile.TemporaryDirectory() )
    tmpdir = auto.pathlib.Path(tmpdir)

    has_tmux = auto.shutil.which('tmux') is not None

    canary = tmpdir / '__terminal_canary'


    if isinstance(args, str):
        if verbose:
            print('$', args)

        args = ['bash', '-c', args, '<bash -c>']

    else:
        if verbose:
            print('$', auto.shlex.join(map(str, args)))

    assert isinstance(args, list), type(args)

    args = [
        'bash', '-c', (
            r'''onexit() { touch "${canary:?}"; }; '''
            r'''canary=${1:?}; shift; '''
            r'''trap onexit EXIT; '''
            r'''"${@:?}"'''
        ), '<bash -c>', *[
            canary,
            *args,
        ],
    ]

    if isinstance(args, list):
        args = auto.shlex.join(map(str, args))
    assert isinstance(args, str), type(args)

    if has_tmux:
        process = auto.subprocess.run([
            'tmux', 'list-sessions',
        ], stdin=auto.subprocess.DEVNULL, stdout=auto.subprocess.PIPE, check=False)

        if process.returncode != 0:
            try:
                get_ipython
            except NameError:
                auto.subprocess.run([
                    'tmux', 'new-session', '-d', '-s', '0',
                ], check=True)
            else:
                get_ipython().system('tmux new-session -d -s 0')

    if has_tmux:
        args = [
            'tmux', 'send-keys', *[
                args,
                'C-m',
            ],
        ]
    else:
        args = [
            'bash', '-c', args,
        ]

    try:
        get_ipython
    except NameError:
        auto.subprocess.run(
            args,
            check = True,
        )
    else:
        get_ipython().system('{auto.shlex.join(args)}')

    while True:
        if canary.exists():
            break

        auto.time.sleep(0.1)

    canary.unlink()


@with_exit_stack
def scp(
    *args,
    verbose: bool = True,
    key: str | auto.typing.Literal[...] | None = ...,
    key_name: str = 'SSH_KEY',
       enter,
):
    if key is ...:
        key = auto.mediocreatbest.getkey(key_name)
        key = auto.base64.b64decode(key)

    if key is not None:
        tmp = enter( auto.tempfile.TemporaryDirectory() )
        tmp = auto.pathlib.Path(tmp)

        tmp_key = tmp / 'id_rsa'
        tmp_key.write_bytes(key)
        tmp_key.chmod(0o600)

        args = [
            '-i', tmp_key,
            *args,
        ]

    canary = tmp / 'canary'
    name = f'scp-{auto.uuid.uuid4()}'

    args = [
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'UserKnownHostsFile=/dev/null',
        '-o', 'BatchMode=yes',
        *args,
    ]

    args = [
        'scp',
        *args,
    ]

    print(f'$ {auto.shlex.join(map(str, args))}')

    # args = [
    #     'bash', '-c', auto.textwrap.dedent(r'''
    #         set -euo pipefail

    #         canary=${1:?}; shift
    #         onexit() { touch "${canary:?}"; }
    #         trap onexit EXIT

    #         cd /content
    #         "${@:?}"
    #     '''), '<bash -c>', *[
    #         canary,
    #     ],
    #     'tmux', 'new-window', *[
    #         '-t', f'1',
    #         '-n', name,
    #         *args,
    #     ],
    # ]

    # !{auto.shlex.join(map(str, args))}

    auto.mediocreatbest.terminal(
        args,
        verbose = False,
    )

    # while not canary.exists():
    #     auto.time.sleep(0.1)


def summary(
    arg,
    /,
) -> str:
    is_pandas = isinstance(arg, auto.pd.DataFrame)
    if is_pandas:
        return summary_pandas_DataFrame(arg)

    is_sqlite3 = any([
        isinstance(arg, auto.sqlite3.Connection),
        all([
            hasattr(arg, 'execute'),
            hasattr(arg, 'commit'),
        ]),
    ])
    if is_sqlite3:
        return summary_sqlite3_Connection(arg)

    assert False, type(arg)


def summary_pandas_DataFrame(
    df,
    /,
) -> str:
    if len(df) > 3:
        df = df.sample(3, random_state=1337)

    df = df.T

    with auto.warnings.catch_warnings():
        auto.warnings.simplefilter('ignore', FutureWarning)

        df = df.applymap(str)
        df = df.applymap(lambda s: auto.textwrap.shorten(s, 72//2))

    return df.to_markdown()


@with_exit_stack
def summary_sqlite3_Connection(
    conn,
    /,
    *,   enter,
) -> str:
    enter( auto.contextlib.redirect_stdout(
        (io := auto.io.StringIO()),
    ) )

    df = auto.pd.read_sql(auto.mediocreatbest.SQLQuery(r'''
        PRAGMA database_list
    '''), conn)

    df.set_index([
        'seq',
    ], inplace=True)
    df.sort_index(inplace=True)

    first = True
    for _seq, row in df.iterrows():
        schema_name = row['name']

        df = auto.pd.read_sql(auto.mediocreatbest.SQLQuery(r'''
            SELECT *
            FROM {{ schema_name |tosqlref }}.sqlite_master
        ''', schema_name=schema_name), conn)

        df.set_index([
            'type',
            'name',
        ], inplace=True)

        df.sort_values([
            'rootpage',
        ], inplace=True)

        for (type, name), row in df.iterrows():
            if type == 'table':
                table_name = row['tbl_name']

                if table_name.startswith('sqlite_'):
                    continue
                if table_name.startswith('sqlean_'):
                    continue

                count ,= conn.execute(auto.mediocreatbest.SQLQuery(r'''
                    SELECT
                        MAX(ROWID)
                    FROM {{ schema_name |tosqlref }}.{{ table_name |tosqlref }}
                    LIMIT 1
                ''', schema_name=schema_name, table_name=table_name)).fetchone()

                assert count is not None, (schema_name, table_name)

                rowids = auto.random.Random(1337).sample(range(1, count + 1), 3)

                df = auto.pd.read_sql(auto.mediocreatbest.SQLQuery(r'''
                    SELECT
                        *
                        , ROWID AS rowid
                    FROM {{ schema_name |tosqlref }}.{{ table_name |tosqlref }}
                    WHERE ROWID IN (
                        {%- set sep = joiner(", ") %}
                        {%- for rowid in rowids %}
                        {{ sep() }}{{ rowid |tosqlint }}
                        {%- endfor %}
                    )
                ''', schema_name=schema_name, table_name=table_name, rowids=rowids), conn)

                df.set_index([
                    'rowid',
                ], inplace=True)
                df.sort_index(inplace=True)

                text = summary(df)

                ref = auto.mediocreatbest.SQLQuery(r'''
                    {{ schema_name |tosqlref }}.{{ table_name |tosqlref }} ({{ count }})
                ''', schema_name=schema_name, table_name=table_name, count=count)
                ref = ref.strip()

                text = auto.re.sub(r'''
                    \|\s+\|
                ''', f'| {ref} |', text, count=1, flags=auto.re.VERBOSE)

                if not first:
                    print()
                    print('---')
                    print()
                else:
                    first = False

                print(text)

            elif type == 'index':
                print(row['sql'])
                if not first:
                    print()
                    print('---')
                    print()
                else:
                    first = False
                print()

    return io.getvalue()


@with_exit_stack
def df2sql(
    df: auto.pd.DataFrame,
    name: str,
    conn: auto.sqlite3.Connection,
    *,   enter,
    batch: int = 10_000,
    verbose: bool = True,
    index: bool = True,
    if_exists: str = 'replace',
):
    count = len(df)

    it = (
        (beg, min(count, beg + batch))
        for beg in range(0, len(df), batch)
    )

    if verbose:
        pbar = enter( auto.tqdm.auto.tqdm(
            total=len(df),
            unit='row',
            unit_scale=True,
        ) )

    for i, (beg, end) in enumerate(it):
        if verbose:
            pbar.update(end - beg)

        df.iloc[beg:end].to_sql(
            name,
            conn,
            if_exists=(
                if_exists
            ) if i == 0 else (
                'append'
            ),
            index=index,
        )

    conn.commit()


#@title Random

class _Random(auto.random.Random):
    def __int__(self) -> int:
        return self.getrandbits(64)


def Random(*seeds: int) -> _Random:
    assert len(seeds) > 0, len(seeds)
    seed = auto.json.dumps(seeds, separators=(',', ':'))
    seed = auto.hashlib.md5(seed.encode()).digest()

    random = _Random(seed)

    return random
