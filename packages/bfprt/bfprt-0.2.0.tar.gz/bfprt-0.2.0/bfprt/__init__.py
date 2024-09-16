import importlib.metadata

from bfprt.algo import select_fast

__version__ = importlib.metadata.version("bfprt")

__all__ = [
    "__version__",
    "select_fast",
]
