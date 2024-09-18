#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from functools import wraps
from math import floor, log10
from typing import Any, Callable, cast, Dict, List, Optional, TypeVar

from langchain.globals import get_llm_cache, set_llm_cache
import langchain_core.caches


def round_sig_figs(value: Any, coerce: bool = False, n: int = 2) -> str:
    """LLM prompt helper function for rounding pd.Series to n sig figs.

    Parameters
    ----------
    value : Any
        value to attempt to format as str with 2 sig figs
    coerce : bool (default=False)
        Whether to attempt to coerce value to float before formatting
    n : int
        Number of sig figs to trim to

    Notes
    -----
    Too much precision seems to increase the risk of hallucinations in
    certain applications (e.g. table extraction/summarization).
    """
    if coerce:
        try:
            value = float(value)
        except ValueError:
            pass
    if value == 0:
        return "0"
    try:
        # thanks stackoverflow
        rounded = round(value, n - int(floor(log10(abs(value)))) - 1)
        if rounded >= 10:
            rounded = int(rounded)
        as_str = repr(rounded)
        if as_str.endswith(".0"):
            as_str = as_str[:-2]
        return as_str
    except TypeError:
        return value  # type: ignore[no-any-return]


F = TypeVar("F", bound=Callable[..., Any])


def with_llm_cache(
    cache: Optional[langchain_core.caches.BaseCache],
) -> Callable[[Callable[..., Any]], F]:
    """Decorator for applying a custom llm cache for the duration of the function."""

    def outer_wrapper(f: F) -> F:
        @wraps(f)
        def inner_wrapper(*args, **kwargs) -> Any:  # type: ignore[no-untyped-def]
            llm_cache = get_llm_cache()
            set_llm_cache(cache)
            try:
                return f(*args, **kwargs)
            finally:
                set_llm_cache(llm_cache)

        if cache is not None:
            return cast(F, inner_wrapper)
        else:
            return f

    return cast(Callable[..., F], outer_wrapper)


# Stop gap until this guy is merged: https://github.com/hwchase17/langchain/pull/1930/
class InMemoryEmbeddingsCache:
    """Cache that stores things in memory."""

    def __init__(self) -> None:
        """Initialize with empty cache."""
        self._cache: Dict[int, Optional[List[float]]] = {}

    def lookup(self, text: str) -> Optional[List[float]]:
        """Look up based on text hash."""
        h = hash(text.encode())
        return self._cache.get(h, None)

    def update(self, text: str, embeddings: List[float]) -> None:
        """Update cache with embeddings from text."""
        h = hash(text.encode())
        self._cache[h] = embeddings

    def clear(self) -> None:
        """Clear the cache."""
        self._cache = {}


def with_embedding_cache(
    cache: bool = True,
) -> Callable[[Callable[..., Any]], Any]:
    """
    Decorator for applying a custom llm cache for the duration of the function.

    Functions using this are in charge of cleaning the cache.
    """
    # Start caching at decoration time

    def outer_wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def inner_wrapper(*args, **kwargs) -> Any:  # type: ignore[no-untyped-def]
            cached = _embedding_cache.lookup(*args, **kwargs)
            if cached is not None:
                return cached
            res = f(*args, **kwargs)
            _embedding_cache.update(*args, embeddings=res)  # type: ignore[misc]
            return res

        if cache:
            return inner_wrapper
        else:
            return f

    return outer_wrapper


_embedding_cache = InMemoryEmbeddingsCache()
