"""
auto: Automatic Importer (and Package Installer)
"""

from __future__ import annotations
from functools import cached_property

__all__ = [
    'auto',
]


class AutoInstallError(ImportError):
    pass

class AutoInstall(object):
    __install_names: ClassVar[dict[str, list[str]]] = {}
    __import_names: ClassVar[dict[str, list[str]]] = {}

    # XXX(th): My Jupyter notebooks keep crashing when Google Colab tries to access
    # these properties, and AutoInstall tries to install it. Hopefully this fixes that
    # problem.
    __custom_documentations__ = {}
    __wrapped__ = None

    @classmethod
    def __register(
        cls,
        *,
        name: str,
        install_names: list[str],
        import_names: list[str],
    ):
        cls.__install_names[name] = install_names
        cls.__import_names[name] = import_names

    @classmethod
    def register(
        cls,
        name: str,
        *extra_names: list[str],
        install_names: list[str]=None,
        import_names: list[str]=None,
    ):
        if install_names is None:
            install_names = []

        if import_names is None:
            import_names = []

        for extra_name in extra_names:
            if '.' in extra_name:
                import_names.append(extra_name)

            else:
                install_names.append(extra_name)

        if not install_names:
            install_names.append(name)

        if not import_names:
            import_names.append(name)

        cls.__register(
            name=name,
            install_names=install_names,
            import_names=import_names,
        )

    def __import(self, name: str):
        import importlib

        import_names = self.__import_names.get(name, [name])
        modules = []
        for import_name in import_names:
            module = importlib.import_module(import_name)
            modules.append(module)

        return modules[0]

    def __install(self, name: str):
        import pip, warnings

        install_names = self.__install_names.get(name, [name])
        with warnings.catch_warnings():
            auto.warnings.simplefilter(action='ignore', category=DeprecationWarning)
            pip.main([
                'install',
                '--quiet',
                *install_names,
            ])

    def __getitem__(self, name: str):
        return getattr(self, name)

    def __getattr__(self, name: str):
        import subprocess, importlib, sys

        module = None
        try:
            module = self.__import(name)

        except ImportError as e:
            self.__install(name)
            module = self.__import(name)

        assert module is not None
        setattr(self, name, module)
        return module

AutoInstall.register('langchain', import_names=[
    'langchain',

    'langchain.adapters', 'langchain.agents', 'langchain._api',
    'langchain.callbacks', 'langchain.chains', 'langchain.chat_loaders',
    'langchain.chat_models', 'langchain.docstore',
    'langchain.document_loaders', 'langchain.document_transformers',
    'langchain.embeddings', 'langchain.evaluation', 'langchain.globals',
    'langchain.graphs', 'langchain.indexes', 'langchain.llms',
    'langchain.load', 'langchain.memory', 'langchain.output_parsers',
    'langchain.prompts', 'langchain.pydantic_v1', 'langchain.retrievers',
    'langchain.runnables', 'langchain.schema', 'langchain.smith',
    'langchain.storage', 'langchain.tools', 'langchain.utilities',
    'langchain.utils', 'langchain.vectorstores',

#     'langchain.agents.agent_toolkits', 'langchain.agents.chat',
#     'langchain.agents.conversational',
#     'langchain.agents.conversational_chat',
#     'langchain.agents.format_scratchpad', 'langchain.agents.mrkl',
#     'langchain.agents.openai_functions_agent',
#     'langchain.agents.openai_functions_multi_agent',
#     'langchain.agents.output_parsers', 'langchain.agents.react',
#     'langchain.agents.self_ask_with_search',
#     'langchain.agents.structured_chat', 'langchain.agents.xml',
#     'langchain.callbacks.streamlit', 'langchain.callbacks.tracers',
#     'langchain.chains.api', 'langchain.chains.chat_vector_db',
#     'langchain.chains.combine_documents',
#     'langchain.chains.constitutional_ai', 'langchain.chains.conversation',
#     'langchain.chains.conversational_retrieval',
#     'langchain.chains.elasticsearch_database', 'langchain.chains.flare',
#     'langchain.chains.graph_qa', 'langchain.chains.hyde',
#     'langchain.chains.llm_bash', 'langchain.chains.llm_checker',
#     'langchain.chains.llm_math',
#     'langchain.chains.llm_summarization_checker',
#     'langchain.chains.llm_symbolic_math', 'langchain.chains.natbot',
#     'langchain.chains.openai_functions', 'langchain.chains.qa_generation',
#     'langchain.chains.qa_with_sources',
#     'langchain.chains.query_constructor',
#     'langchain.chains.question_answering', 'langchain.chains.retrieval_qa',
#     'langchain.chains.router', 'langchain.chains.sql_database',
#     'langchain.chains.summarize', 'langchain.document_loaders.blob_loaders',
#     'langchain.document_loaders.parsers', 'langchain.evaluation.agents',
#     'langchain.evaluation.comparison', 'langchain.evaluation.criteria',
#     'langchain.evaluation.embedding_distance',
#     'langchain.evaluation.exact_match', 'langchain.evaluation.parsing',
#     'langchain.evaluation.qa', 'langchain.evaluation.regex_match',
#     'langchain.evaluation.scoring', 'langchain.evaluation.string_distance',
#     'langchain.indexes.prompts', 'langchain.memory.chat_message_histories',
#     'langchain.prompts.example_selector',
#     'langchain.retrievers.document_compressors',
#     'langchain.retrievers.self_query', 'langchain.schema.runnable',
#     'langchain.smith.evaluation', 'langchain.tools.amadeus',
#     'langchain.tools.arxiv', 'langchain.tools.azure_cognitive_services',
#     'langchain.tools.bearly', 'langchain.tools.bing_search',
#     'langchain.tools.brave_search', 'langchain.tools.clickup',
#     'langchain.tools.dataforseo_api_search', 'langchain.tools.ddg_search',
#     'langchain.tools.e2b_data_analysis', 'langchain.tools.edenai',
#     'langchain.tools.eleven_labs', 'langchain.tools.file_management',
#     'langchain.tools.github', 'langchain.tools.gitlab',
#     'langchain.tools.gmail', 'langchain.tools.golden_query',
#     'langchain.tools.google_places', 'langchain.tools.google_scholar',
#     'langchain.tools.google_search', 'langchain.tools.google_serper',
#     'langchain.tools.graphql', 'langchain.tools.human',
#     'langchain.tools.interaction', 'langchain.tools.jira',
#     'langchain.tools.json', 'langchain.tools.metaphor_search',
#     'langchain.tools.multion', 'langchain.tools.nuclia',
#     'langchain.tools.office365', 'langchain.tools.openapi',
#     'langchain.tools.openweathermap', 'langchain.tools.playwright',
#     'langchain.tools.powerbi', 'langchain.tools.pubmed',
#     'langchain.tools.python', 'langchain.tools.requests',
#     'langchain.tools.scenexplain', 'langchain.tools.searchapi',
#     'langchain.tools.searx_search', 'langchain.tools.shell',
#     'langchain.tools.sleep', 'langchain.tools.spark_sql',
#     'langchain.tools.sql_database',
#     'langchain.tools.steamship_image_generation',
#     'langchain.tools.tavily_search', 'langchain.tools.vectorstore',
#     'langchain.tools.wikipedia', 'langchain.tools.wolfram_alpha',
#     'langchain.tools.youtube', 'langchain.tools.zapier',
#     'langchain.vectorstores.docarray', 'langchain.vectorstores.redis'
])

AutoInstall.register('tf', import_names=[
    'tensorflow',
])

AutoInstall.register('google', import_names=[
    'google', 'google.colab', 'google.colab.syntax', 'google.colab.userdata',
])

AutoInstall.register('tk', import_names=[
    'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.dnd',
    'tkinter.font', 'tkinter.tix', 'tkinter.colorchooser',
    'tkinter.messagebox',
])

AutoInstall.register('tkinter', import_names=[
    'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.dnd',
    'tkinter.font', 'tkinter.tix', 'tkinter.colorchooser',
    'tkinter.messagebox',
])

AutoInstall.register('ttk', import_names=[
    'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.dnd',
    'tkinter.font', 'tkinter.tix', 'tkinter.colorchooser',
    'tkinter.messagebox',
])

AutoInstall.register('np', install_names=['numpy'], import_names=['numpy'])
AutoInstall.register('pd', install_names=['pandas'], import_names=['pandas'])

AutoInstall.register('tqdm', import_names=['tqdm', 'tqdm.auto', 'tqdm.notebook'])

for pyplot_name in ['pyplot', 'plt']:
    AutoInstall.register(pyplot_name, install_names=['matplotlib'], import_names=['matplotlib.pyplot'])
AutoInstall.register('matplotlib', import_names=[
    'matplotlib',
    'matplotlib.pyplot',
])

# Thanks https://docs.scipy.org/doc/scipy/reference/index.html
#   (() => {
#     const texts = [];
#     for (const $el of $$('ul.nav > li.toctree-l1 > a.reference.internal')) {
#       texts.push(`  "${$el.textContent.trim()}",`);
#     }
#     console.log(texts.join("\n"));
#   })();
AutoInstall.register('scipy', import_names=[
    "scipy",
    "scipy.cluster",
    "scipy.constants",
    "scipy.datasets",
    "scipy.fft",
    "scipy.fftpack",
    "scipy.integrate",
    "scipy.interpolate",
    "scipy.io",
    "scipy.linalg",
    "scipy.misc",
    "scipy.ndimage",
    "scipy.odr",
    "scipy.optimize",
    "scipy.signal",
    "scipy.sparse",
    "scipy.spatial",
    "scipy.special",
    "scipy.stats",
])

# Thanks https://scikit-learn.org/stable/modules/classes.html
#   (() => {
#   const texts = [];
#   for (const $el of $$('code.xref.py.py-mod.docutils.literal.notranslate > span.pre')) {
#     texts.push(`  "${$el.textContent}",`);
#   }
#   console.log(texts.join("\n"));
#   })();
AutoInstall.register('sklearn', import_names=[
    "sklearn",
    "sklearn.base",
    "sklearn.calibration",
    "sklearn.cluster",
    "sklearn.compose",
    "sklearn.covariance",
    "sklearn.cross_decomposition",
    "sklearn.datasets",
    "sklearn.decomposition",
    "sklearn.discriminant_analysis",
    "sklearn.dummy",
    "sklearn.ensemble",
    "sklearn.exceptions",
    "sklearn.experimental",
    "sklearn.feature_extraction",
    "sklearn.feature_selection",
    "sklearn.gaussian_process",
    "sklearn.impute",
    "sklearn.inspection",
    "sklearn.isotonic",
    "sklearn.kernel_approximation",
    "sklearn.kernel_ridge",
    "sklearn.linear_model",
    "sklearn.manifold",
    "sklearn.metrics",
    "sklearn.mixture",
    "sklearn.model_selection",
    "sklearn.multiclass",
    "sklearn.multioutput",
    "sklearn.naive_bayes",
    "sklearn.neighbors",
    "sklearn.neural_network",
    "sklearn.pipeline",
    "sklearn.preprocessing",
    "sklearn.random_projection",
    "sklearn.semi_supervised",
    "sklearn.svm",
    "sklearn.tree",
    "sklearn.utils",
    "sklearn.base",
    "sklearn.calibration",
    "sklearn.cluster",
    "sklearn.cluster",
    "sklearn.compose",
    "sklearn.covariance",
    "sklearn.covariance",
    "sklearn.cross_decomposition",
    "sklearn.datasets",
    "sklearn.datasets",
    "sklearn.decomposition",
    "sklearn.decomposition",
    "sklearn.discriminant_analysis",
    "sklearn.dummy",
    "sklearn.ensemble",
    "sklearn.ensemble",
    "sklearn.exceptions",
    "sklearn.exceptions",
    "sklearn.experimental",
    "sklearn.experimental",
    "sklearn.feature_extraction",
    "sklearn.feature_extraction",
    "sklearn.feature_extraction.image",
    "sklearn.feature_extraction.text",
    "sklearn.feature_selection",
    "sklearn.feature_selection",
    "sklearn.gaussian_process",
    "sklearn.gaussian_process",
    "sklearn.impute",
    "sklearn.inspection",
    "sklearn.inspection",
    "sklearn.isotonic",
    "sklearn.kernel_approximation",
    "sklearn.kernel_approximation",
    "sklearn.kernel_ridge",
    "sklearn.kernel_ridge",
    "sklearn.linear_model",
    "sklearn.linear_model",
    "sklearn.manifold",
    "sklearn.manifold",
    "sklearn.metrics",
    "sklearn.metrics",
    "sklearn.metrics.cluster",
    "sklearn.mixture",
    "sklearn.mixture",
    "sklearn.model_selection",
    "sklearn.multiclass",
    "sklearn.multioutput",
    "sklearn.naive_bayes",
    "sklearn.naive_bayes",
    "sklearn.neighbors",
    "sklearn.neighbors",
    "sklearn.neural_network",
    "sklearn.neural_network",
    "sklearn.pipeline",
    "sklearn.pipeline",
    "sklearn.preprocessing",
    "sklearn.preprocessing",
    "sklearn.random_projection",
    "sklearn.semi_supervised",
    "sklearn.semi_supervised",
    "sklearn.svm",
    "sklearn.svm",
    "sklearn.tree",
    "sklearn.tree",
    "sklearn.utils",
    "sklearn.utils",
])

AutoInstall.register('PIL', install_names=['pillow'], import_names=[
    'PIL',
    'PIL.BmpImagePlugin',
    'PIL.ExifTags',
    'PIL.GifImagePlugin',
    'PIL.GimpGradientFile',
    'PIL.GimpPaletteFile',
    'PIL.Image',
    'PIL.ImageChops',
    'PIL.ImageColor',
    'PIL.ImageFile',
    'PIL.ImageMode',
    'PIL.ImageOps',
    'PIL.ImagePalette',
    'PIL.ImageSequence',
    'PIL.JpegImagePlugin',
    'PIL.JpegPresets',
    'PIL.PaletteFile',
    'PIL.PngImagePlugin',
    'PIL.PpmImagePlugin',
    'PIL.TiffImagePlugin',
    'PIL.TiffTags',
])

machine_learning_packages = [
    'transformers',
    'accelerate',
    'datasets',
    'tokenizers',
    'evaluate',
    'huggingface_hub',
    'torch',
]
for machine_learning_package in machine_learning_packages:
    AutoInstall.register(machine_learning_package, install_names=machine_learning_packages)

autoinstall = AutoInstall()


#---

class AutoImport:
    @cached_property
    def importlib(auto):
        import importlib
        return importlib

    def __getattr__(auto, name: str):
        return auto.importlib.import_module(name)

    def numpy(auto):
        import numpy
        import numpy.lib.recfunctions
        return numpy

    def np(auto):
        return auto.numpy

    def pd(auto):
        return auto.pandas

    def sklearn(auto):
        import sklearn
        import sklearn.base
        import sklearn.calibration
        import sklearn.cluster
        import sklearn.compose
        import sklearn.covariance
        import sklearn.cross_decomposition
        import sklearn.datasets
        import sklearn.decomposition
        import sklearn.discriminant_analysis
        import sklearn.dummy
        import sklearn.dummy
        import sklearn.ensemble
        import sklearn.ensemble
        import sklearn.exceptions
        import sklearn.experimental
        import sklearn.feature_extraction
        import sklearn.feature_extraction.image
        import sklearn.feature_extraction.text
        import sklearn.gaussian_process
        import sklearn.impute
        import sklearn.inspection
        import sklearn.isotonic
        import sklearn.kernel_approximation
        import sklearn.kernel_ridge
        import sklearn.linear_model
        import sklearn.manifold
        import sklearn.metrics
        import sklearn.metrics.cluster
        import sklearn.mixture
        import sklearn.model_selection
        import sklearn.multiclass
        import sklearn.multioutput
        import sklearn.naive_bayes
        import sklearn.neighbors
        import sklearn.neural_network
        import sklearn.pipeline
        import sklearn.preprocessing
        import sklearn.random_projection
        import sklearn.semi_supervised
        import sklearn.svm
        import sklearn.tree
        import sklearn.utils
        return sklearn

    def scipy(auto):
        import scipy
        import scipy.cluster
        import scipy.constants
        import scipy.datasets
        import scipy.fft
        import scipy.fftpack
        import scipy.integrate
        import scipy.interpolate
        import scipy.io
        import scipy.linalg
        import scipy.misc
        import scipy.ndimage
        import scipy.odr
        import scipy.optimize
        import scipy.signal
        import scipy.sparse
        import scipy.spatial
        import scipy.special
        import scipy.stats
        return scipy

    def mpl(auto):
        return auto.matplotlib

    def plt(auto):
        return auto.matplotlib.pyplot
    
    def PIL(auto):
        import PIL
        import PIL.BmpImagePlugin
        import PIL.ExifTags
        import PIL.GifImagePlugin
        import PIL.GimpGradientFile
        import PIL.GimpPaletteFile
        import PIL.Image
        import PIL.ImageChops
        import PIL.ImageColor
        import PIL.ImageFile
        import PIL.ImageMode
        import PIL.ImageOps
        import PIL.ImagePalette
        import PIL.ImageSequence
        import PIL.JpegImagePlugin
        import PIL.JpegPresets
        import PIL.PaletteFile
        import PIL.PngImagePlugin
        import PIL.PpmImagePlugin
        import PIL.TiffImagePlugin
        import PIL.TiffTags
        return PIL

    def tqdm(auto):
        import tqdm
        import tqdm.auto
        import tqdm.notebook
        return tqdm

    def tkinter(auto):
        import tkinter
        import tkinter.ttk
        import tkinter.scrolledtext
        import tkinter.dnd
        import tkinter.font
        import tkinter.tix
        import tkinter.colorchooser
        import tkinter.messagebox
        return tkinter

    def google(auto):
        import google
        import google.colab
        import google.colab.syntax
        import google.colab.userdata
        return google

autoimport = AutoImport()


#---

try:
    get_ipython
except NameError:
    auto = autoimport
else:
    auto = autoinstall
