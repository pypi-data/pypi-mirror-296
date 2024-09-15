import json
from pathlib import Path
from typing import Any, List, Literal, Optional

from keble_helpers import hash_string

MethodNames = Literal["aembed_query", "embed_query", "aembed_documents", "embed_documents"]


class MockEmbeddings:
    def __init__(self, *, name: str, cache_dir: str | Path, embeddings_model: Any):
        """
        Initialize the embedding manager with a name, cache directory, and an embedding model (real or mock).
        """
        self.name = name
        self.cache_dir = Path(cache_dir)
        self.embeddings_model = embeddings_model
        self.cache_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        self.cached_responses = {}

        # Load existing cached responses if available
        self.load_cache()

    @property
    def cache_filename(self) -> str:
        return f"{self.name}_embeddings.json"

    def load_cache(self):
        """
        Load cached embeddings from the directory (if they exist).
        """
        cache_file = self.cache_dir / self.cache_filename
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                self.cached_responses = json.load(f)

    def save_cache(self):
        """
        Save the cached embeddings to a .json file in the cache directory.
        """
        cache_file = self.cache_dir / self.cache_filename
        with open(cache_file, 'w') as f:
            json.dump(self.cached_responses, f)

    def get_cache_key(self, method_name: MethodNames, args: Any, kwargs: Any) -> str:
        """
        Generate a unique cache key based on method name and input arguments.
        """
        return f"{method_name}_{hash_string(str(args) + str(kwargs))}"

    def load_from_cache(self, method_name: MethodNames, *args: Any, **kwargs: Any) -> Optional[Any]:
        """
        Load the cached embeddings for the given method and input arguments.
        """
        cache_key = self.get_cache_key(method_name, args, kwargs)
        return self.cached_responses.get(cache_key)

    def save_as_cache(self, method_name: MethodNames, result: Any, *args: Any, **kwargs: Any):
        """
        Save the result of an embedding method call to the cache.
        """
        cache_key = self.get_cache_key(method_name, args, kwargs)
        self.cached_responses[cache_key] = result
        self.save_cache()

    def embed_query(self, *args: Any, **kwargs: Any) -> List[float]:
        """
        Embed a query using either the cached result or the real embedding model.
        """
        cached_result = self.load_from_cache("embed_query", *args, **kwargs)
        if cached_result:
            return cached_result
        else:
            result = self.embeddings_model.embed_query(*args, **kwargs)
            self.save_as_cache("embed_query", result, *args, **kwargs)
            return result

    def embed_documents(self, *args: Any, **kwargs: Any) -> List[List[float]]:
        """
        Embed documents using either the cached result or the real embedding model.
        """
        cached_result = self.load_from_cache("embed_documents", *args, **kwargs)
        if cached_result:
            return cached_result
        else:
            result = self.embeddings_model.embed_documents(*args, **kwargs)
            self.save_as_cache("embed_documents", result, *args, **kwargs)
            return result

    async def aembed_query(self, *args: Any, **kwargs: Any) -> List[float]:
        """
        Asynchronously embed a query using either the cached result or the real embedding model.
        """
        cached_result = self.load_from_cache("aembed_query", *args, **kwargs)
        if cached_result:
            return cached_result
        else:
            result = self.embeddings_model.aembed_query(*args, **kwargs)
            if not isinstance(result, list):
                result = await result
            self.save_as_cache("aembed_query", result, *args, **kwargs)
            return result

    async def aembed_documents(self, *args: Any, **kwargs: Any) -> List[List[float]]:
        """
        Asynchronously embed documents using either the cached result or the real embedding model.
        """
        cached_result = self.load_from_cache("aembed_documents", *args, **kwargs)
        if cached_result:
            return cached_result
        else:
            result = self.embeddings_model.aembed_documents(*args, **kwargs)
            if not isinstance(result, list):
                result = await result
            self.save_as_cache("aembed_documents", result, *args, **kwargs)
            return result

    def reset_cache(self):
        """
        Clear all cached responses and reset the cache.
        """
        self.cached_responses = {}
        self.save_cache()

    def teardown(self):
        """
        Tear down any active resources and reset the cache.
        """
        self.reset_cache()
