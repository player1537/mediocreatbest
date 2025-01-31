#@title LLM { display-mode: "form" }

def LLM(
    arg: str | None = None,
    /,
    *,
    api_url: str | auto.typing.Literal[...] = ...,
    api_key: str | None | auto.typing.Literal[...] = ...,
    api_key_name: str = 'LLAMA_API_KEY',
    cache: auto.typing.Literal[...] | None = ...,
) -> _LLM:
    host, model = arg.split('/', 1)

    if api_url is ...:
        api_url = {
            ('devcloud', 'llama'):
                'https://completion.on.devcloud.is.mediocreatbest.xyz/llama/',
            ('sahara', 'llama'):
                'https://completion.on.sahara.is.mediocreatbest.xyz/llama/',
            ('kavir', 'llama'):
                'https://completion.on.kavir.is.mediocreatbest.xyz/llama/',
            ('nebula', 'llama'):
                'https://completion.on.nebula.is.mediocreatbest.xyz/llama/',

            ('sahara', 'tinyllama'):
                'https://completion.on.sahara.is.mediocreatbest.xyz/tinyllama/',
            ('kavir', 'tinyllama'):
                'https://completion.on.kavir.is.mediocreatbest.xyz/tinyllama/',
            ('nebula', 'tinyllama'):
                'https://completion.on.nebula.is.mediocreatbest.xyz/tinyllama/',

            ('sahara', 'nomic'):
                'https://completion.on.sahara.is.mediocreatbest.xyz/nomic/',
            ('kavir', 'nomic'):
                'https://completion.on.kavir.is.mediocreatbest.xyz/nomic/',
            ('nebula', 'nomic'):
                'https://completion.on.nebula.is.mediocreatbest.xyz/nomic/',

            ('sahara', 'SFR-Embedding-Mistral'):
                'https://completion.on.sahara.is.mediocreatbest.xyz/SFR-Embedding-Mistral/',
        }[host, model]

    if api_key is ...:
        api_key = auto.mediocreatbest.getkey(api_key_name)

    if cache is ...:
        global __LLM_cache
        try: __LLM_cache
        except NameError: __LLM_cache = None
        if __LLM_cache is None:
            __LLM_cache = {}
        if model not in __LLM_cache:
            __LLM_cache[model] = auto.shelve.open(f'LLM.{model}.shelve', 'c')
        cache = __LLM_cache[model]

    prompt_kwargs = dict(
        max_tokens=300,
        temperature=0.0,
        # top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        cache_prompt=True,
    ) | {
        'llama': dict(
            stop=[
                '<|eot_id|>',
            ],
        ),
        'tinyllama': dict(
            stop=[
                # '</s>',
                '<|endoftext|>',
                '<|im_end|>',
            ],
        ),
    }.get(model, {})

    llm = _LLM(
        model=model,
        api_url=api_url,
        api_key=api_key,
        cache=cache,
        prompt_kwargs=prompt_kwargs,
    )

    return llm


class _LLM:
    """
    A class for interacting with a language model API to generate completions and embeddings.

    The LLM class provides methods to send prompts to a language model API and retrieve the
    generated completions or embeddings. It handles the details of the API request and response,
    and provides options for caching results to avoid redundant API calls.

    Parameters
    ----------
    model : str or None, default=None
        The name of the language model to use for generating completions and embeddings.
        If None, the model must be specified in each call to `complete` or `embed`.

    api_url : str
        The URL of the API endpoint to use for generating completions and embeddings.

    api_key : str or None, default=...
        The API key to use for authentication when making requests to the API. If not specified,
        the `api_key_name` parameter must be specified to retrieve the key from the Colab
        user data.

    api_key_name : str or None, default=None
        The name of the Colab user data key that stores the API key. If None, the `api_key`
        parameter must be specified directly.

    session : requests.Session or None, default=None
        The `requests.Session` object to use for making API requests. If None, a new session
        will be created.

    prompt_kwargs : dict or None, default=None
        A dictionary of default keyword arguments to use for the `complete` method. These
        arguments will be merged with any arguments specified in each call to `complete`.

    cache : dict or None, default=None
        A dictionary to use as a cache for storing API responses. If None, a new empty
        dictionary will be created.

    Methods
    -------
    complete(**prompt) -> dict
        Generate a completion for the given prompt using the language model API.

    embed(input) -> numpy.ndarray
        Generate embeddings for the given input text or texts using the language model API.

    """

    def __init__(
        self,
        *,
        model: str | None = None,
        api_url: str,
        api_key: str | None | Ellipsis = ...,
        api_key_name: str | None = None,
        session: auto.requests.Session | auto.typing.Literal[...] = ...,
        prompt_kwargs: dict[str, auto.typing.Any] | None = None,
        cache: dict[str, auto.typing.Any] | auto.typing.Literal[...] | None = ...,
        lock: auto.threading.Lock | auto.typing.Literal[...] | None = ...,
    ):
        if api_key is Ellipsis:
            assert api_key_name is not None, \
                "Either 'api_key' or 'api_key_name' must be specified."
            api_key = auto.mediocreatbest.getpass(api_key_name)

        if session is ...:
            session = auto.requests.Session()
        if prompt_kwargs is None:
            prompt_kwargs = {}
        if cache is ...:
            cache = {}
        if lock is ...:
            lock = auto.threading.Lock()

        self.default_model = model
        self.default_api_url = api_url
        self.default_api_key = api_key
        self.default_session = session
        self.default_prompt_kwargs = prompt_kwargs
        self.default_cache = cache
        self.default_lock = lock

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return self is other

    def complete(
        self,
        *,
        api_url: str | auto.typing.Literal[...] = ...,
        api_key: str | None | auto.typing.Literal[...] = ...,
        session: auto.requests.Session | auto.typing.Literal[...] = ...,
        cache: dict[str, auto.typing.Any] | None | auto.typing.Literal[...] = ...,
        model: str | None | auto.typing.Literal[...] = ...,
        lock: auto.threading.Lock | auto.typing.Literal[...] | None = ...,
        **prompt,
    ) -> dict[str, auto.typing.Any]:
        if api_url is Ellipsis:
            api_url = self.default_api_url
        if api_key is Ellipsis:
            api_key = self.default_api_key
        if session is Ellipsis:
            session = self.default_session
        if cache is Ellipsis:
            cache = self.default_cache
        if model is Ellipsis:
            model = self.default_model
        if lock is Ellipsis:
            lock = self.default_lock
        if lock is None:
            lock = auto.contextlib.nullcontext()

        prompt = self.default_prompt_kwargs | prompt
        if model is not None:
            prompt = prompt | dict(
                model=model,
            )

        is_text = 'prompt' in prompt
        is_chat = 'messages' in prompt
        assert is_text != is_chat, \
            "Either 'prompt' or 'messages' must be specified."

        if is_text:
            url = f'{api_url}v1/completions'
        else:
            url = f'{api_url}v1/chat/completions'

        headers = {
            'Content-Type': 'application/json',
        }
        if api_key is not None:
            headers['Authorization'] = f'Bearer {api_key}'

        ckey = auto.json.dumps(prompt, sort_keys=True)
        with lock:
            need = cache is None or ckey not in cache

        if need:
            with session.request(
                'POST',
                url,
                headers=headers,
                json=prompt,
            ) as response:
                try:
                    response.raise_for_status()
                except Exception as e:
                    raise ValueError(f'API error: {response.text}') from e
                output = response.json()

            if cache is not None:
                with lock:
                    cache[ckey] = output

            self.was_cached = False

        else:
            with lock:
                output = cache[ckey]

            self.was_cached = True

        return output

    def embed(
        self,
        input: str | list[str],
        *,
        api_url: str | auto.typing.Literal[...] = ...,
        api_key: str | None | auto.typing.Literal[...] = ...,
        session: auto.requests.Session | auto.typing.Literal[...] = ...,
        cache: dict[str, auto.typing.Any] | auto.typing.Literal[...] = ...,
        model: str | None | Ellipsis = ...,
        lock: auto.threading.Lock | auto.typing.Literal[...] | None = ...,
        verbose: bool | int = False,
    ) -> auto.np.ndarray[float]:
        if api_url is Ellipsis:
            api_url = self.default_api_url
        if api_key is Ellipsis:
            api_key = self.default_api_key
        if session is Ellipsis:
            session = self.default_session
        if cache is Ellipsis:
            cache = self.default_cache
        if model is Ellipsis:
            model = self.default_model
        if lock is Ellipsis:
            lock = self.default_lock
        if lock is None:
            lock = auto.contextlib.nullcontext()
        verbose = int(verbose)

        if isinstance(input, str):
            input = [input]
            one = True
        else:
            one = False

        N = len(input)
        K = 100
        it = (
            (beg, min(N, beg+K))
            for beg in range(0, N, K)
        )

        if verbose >= 1:
            pbar = auto.tqdm.auto.tqdm(total=N)

        embeds = []
        for beg, end in it:
            if verbose >= 1:
                pbar.update(end-beg)

            json = dict(
                input=input[beg:end],
            )
            if model is not None:
                json |= dict(
                    model=model,
                )

            ckey = auto.json.dumps(json, sort_keys=True)
            with lock:
                need = cache is None or ckey not in cache

            if need:
                with session.request(
                    'POST',
                    f'{api_url}v1/embeddings',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {api_key}',
                    },
                    json=json,
                ) as response:
                    response.raise_for_status()
                    output = response.json()

                if cache is not None:
                    with lock:
                        cache[ckey] = output

                self.was_cached = False

            else:
                with lock:
                    output = cache[ckey]

                self.was_cached = True

            for data in output['data']:
                embed = data['embedding']
                embeds.append(embed)

        embeds = auto.np.array(embeds)

        if one:
            embeds = embeds[0]

        return embeds

    def tokenize(
        self,

        input: str,
        *,
        add_special: bool = False,

        api_url: str | auto.typing.Literal[...] = ...,
        api_key: str | None | auto.typing.Literal[...] = ...,
        session: auto.requests.Session | auto.typing.Literal[...] = ...,
        cache: dict[str, auto.typing.Any] | auto.typing.Literal[...] = ...,
        model: str | None | auto.typing.Literal[...] = ...,
        lock: auto.threading.Lock | auto.typing.Literal[...] | None = ...,
    ) -> list[int]:
        if api_url is Ellipsis:
            api_url = self.default_api_url
        if api_key is Ellipsis:
            api_key = self.default_api_key
        if session is Ellipsis:
            session = self.default_session
        if cache is Ellipsis:
            cache = self.default_cache
        if model is Ellipsis:
            model = self.default_model
        if lock is Ellipsis:
            lock = self.default_lock
        if lock is None:
            lock = auto.contextlib.nullcontext()

        url = api_url
        url = f'{url}tokenize'

        json = dict(
            content=input,
            add_special=add_special,
        )
        if model is not None:
            json |= dict(
                model=model,
            )

        ckey = auto.json.dumps(json, sort_keys=True)
        with lock:
            need = cache is None or ckey not in cache

        if need:
            with session.request(
                'POST',
                url,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}',
                },
                json=json,
            ) as response:
                response.raise_for_status()
                json = response.json()

            if cache is not None:
                with lock:
                    cache[ckey] = json

            self.was_cached = False

        else:
            with lock:
                json = cache[ckey]

            self.was_cached = True

        tokens = []
        for token in json['tokens']:
            tokens.append(token)

        return tokens

    def detokenize(
        self,

        tokints: list[int],
        *,
        api_url: str | auto.typing.Literal[...] = ...,
        api_key: str | None | auto.typing.Literal[...] = ...,
        session: auto.requests.Session | auto.typing.Literal[...] = ...,
        cache: dict[str, auto.typing.Any] | auto.typing.Literal[...] = ...,
        lock: auto.threading.Lock | auto.typing.Literal[...] | None = ...,
    ) -> list[str]:
        if api_url is Ellipsis:
            api_url = self.default_api_url
        if api_key is Ellipsis:
            api_key = self.default_api_key
        if session is Ellipsis:
            session = self.default_session
        if cache is Ellipsis:
            cache = self.default_cache
        if lock is Ellipsis:
            lock = self.default_lock
        if lock is None:
            lock = auto.contextlib.nullcontext()

        url = api_url
        url = f'{url}detokenize'

        tokens = []
        for tokint in tokints:
            json = dict(
                tokens=[tokint],
            )

            ckey = auto.json.dumps(json, sort_keys=True)
            with lock:
                need = cache is None or ckey not in cache

            if need:
                with session.request(
                    'POST',
                    url,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {api_key}',
                    },
                    json=json,
                ) as response:
                    response.raise_for_status()
                    json = response.json()

                if cache is not None:
                    with lock:
                        cache[ckey] = json

                self.was_cached = False

            else:
                with lock:
                    json = cache[ckey]

                self.was_cached = True

            token = json['content']

            tokens.append(token)

        return tokens


def scope():
    llm = LLM('sahara/llama')

    prompt = auto.wikipedia.page("Large Language Models").content[:4000]

    prompt = dict(
        messages=[
            { 'role': 'user', 'content': (
                prompt
            ) },
        ],
    ) | dict(
        temperature=0.0,
        max_tokens=1000,
        n_predict=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        cache=None,
    )

    output = llm.complete(**prompt)

    with auto.mediocreatbest.Textarea():
        print(auto.json.dumps(output, indent=4))

# /scope
