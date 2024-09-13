import shutil
from typing import Any

from tecton_gen_ai.utils.config_wrapper import as_config
import logging


def create_testing_vector_db_config(path: str, remove_if_exists: bool) -> Any:
    if remove_if_exists:
        shutil.rmtree(path, ignore_errors=True)

    from langchain_community.vectorstores.lancedb import LanceDB
    from langchain_openai import OpenAIEmbeddings

    LanceDBConf = as_config(LanceDB)
    OpenAIEmbeddingsConf = as_config(OpenAIEmbeddings)

    vdb = LanceDBConf(embedding=OpenAIEmbeddingsConf(), uri=path)
    return vdb


def print_md(text: str) -> None:
    try:
        import rich
        from rich.markdown import Markdown

        rich.print(Markdown(text))
    except ImportError:
        from IPython.display import Markdown, display

        display(Markdown(text))


def make_debug_logger(filter: Any = None) -> logging.Logger:
    from rich.logging import RichHandler

    logger = logging.getLogger("rich_logger")
    logger.setLevel(logging.DEBUG)
    handler = RichHandler(show_time=False)
    logger.handlers.clear()
    logger.addHandler(handler)
    if filter is not None:
        logger.filters.clear()
        logger.addFilter(filter)
    return logger
