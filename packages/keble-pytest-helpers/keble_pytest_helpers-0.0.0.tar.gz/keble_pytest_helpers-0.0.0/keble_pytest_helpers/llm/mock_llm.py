import json
from pathlib import Path
from typing import Any, Union, List, Literal

from keble_helpers import hash_string
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessageChunk, BaseMessage

from ..utils import convert_ai_message_to_dict

MethodNames = Literal["ainvoke", "invoke", "astream", "stream"]


class MockLlm:
    def __init__(self, *, name: str, cache_dir: str | Path, llm: BaseChatModel):
        """
        Initialize the wrapper with a name, cache directory, and real LLM object (AzureChatOpenAI).
        """
        self.name = name
        self.cache_dir = Path(cache_dir)
        self.llm = llm
        self.cache_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        self.cached_responses = {}

        # Load existing cached responses if available
        self.load_cache()

    @property
    def cache_filename(self) -> str:
        return f"{self.name}.json"

    def load_cache(self):
        """
        Load cached responses from the directory (if they exist).
        """
        cache_file = self.cache_dir / self.cache_filename
        if cache_file.exists():
            with open(cache_file, "r") as f:
                try:
                    self.cached_responses = json.load(f)
                except Exception as e:
                    raise ValueError(f"Failed to load cached response from file: {cache_file}. Exception: {e}")
        if self.cached_responses is not None:
            for key, val in self.cached_responses.items():
                if isinstance(val, list):
                    # streaming cache
                    self.cached_responses[key] = [AIMessageChunk(**item) for item in val]
                elif isinstance(val, dict):
                    if "type" not in val or ("type" in val and val['type'] == "ai"):
                        self.cached_responses[key] = AIMessage(**val)  # use ai message
                    else:
                        self.cached_responses[key] = AIMessageChunk(**val)  # use ai message chunk
                else:
                    self.cached_responses[key] = val

    def save_cache(self):
        """
        Save the cached responses to a .json file in the cache directory.
        """
        cache_file = self.cache_dir / self.cache_filename
        _json = {}
        for key, val in self.cached_responses.items():
            if isinstance(val, list):
                _json[key] = [convert_ai_message_to_dict(item) for item in val]
            elif isinstance(val, BaseMessage) or isinstance(val, BaseMessageChunk) or isinstance(val,
                                                                                                 AIMessage) or isinstance(
                val, AIMessageChunk):
                _json[key] = convert_ai_message_to_dict(val)
            else:
                _json[key] = val
        with open(cache_file, "w") as f:
            json.dump(_json, f, indent=4)

    def get_cache_key(self, method_name: MethodNames, args, kwargs):
        """
        Generate a unique cache key based on method name and input arguments.
        """
        return f"{method_name}_{hash_string(str(args) + str(kwargs))}"

    def save_as_cache(self, method_name: MethodNames,
                      result: Union[BaseMessage, List[BaseMessageChunk], AIMessage, List[AIMessageChunk]], *args: Any,
                      **kwargs: Any):
        """
        Save the result of a method call to the cache.
        """

        cache_key = self.get_cache_key(method_name, args, kwargs)
        self.cached_responses[cache_key] = result
        self.save_cache()

    def load_from_cache(self, method_name, *args, **kwargs):
        """
        Load the cached response for the given method and input arguments.
        """
        cache_key = self.get_cache_key(method_name, args, kwargs)
        return self.cached_responses.get(cache_key)

    def invoke(self, *args, **kwargs):
        """
        Mocked version of the LLM's `invoke` method.
        """
        cached_result = self.load_from_cache("invoke", *args, **kwargs)
        if cached_result:
            return cached_result
        else:
            # Call the real LLM method and cache the result
            result = self.llm.invoke(*args, **kwargs)
            self.save_as_cache("invoke", result, *args, **kwargs)
            return result

    def stream(self, *args, **kwargs):
        """
        Mocked version of the LLM's `stream` method.
        """
        cached_result = self.load_from_cache("stream", *args, **kwargs)
        if cached_result:
            yield from cached_result
        else:
            # Call the real LLM method and cache the result
            real_result = list(self.llm.stream(*args, **kwargs))
            self.save_as_cache("stream", real_result, *args, **kwargs)
            yield from real_result

    async def astream(self, *args, **kwargs):
        """
        Mocked version of the LLM's async `astream` method.
        """
        cached_result = self.load_from_cache("astream", *args, **kwargs)
        if cached_result:
            for response in cached_result:
                yield response
        else:
            # Call the real LLM method and cache the result
            real_result = []
            async for response in self.llm.astream(*args, **kwargs):
                real_result.append(response)
                yield response
            self.save_as_cache("astream", real_result, *args, **kwargs)

    async def ainvoke(self, *args, **kwargs):
        """
        Mocked version of the LLM's async `ainvoke` method.
        """
        cached_result = self.load_from_cache("ainvoke", *args, **kwargs)
        if cached_result:
            return cached_result
        else:
            # Call the real LLM method and cache the result
            result = await self.llm.ainvoke(*args, **kwargs)
            self.save_as_cache("ainvoke", result, *args, **kwargs)
            return result

    def reset_cache(self):
        """
        Clear all cached responses and reset the cache.
        """
        self.cached_responses = {}
        self.save_cache()

    def teardown(self):
        """
        Tear down any active mocks and clear resources.
        """
        self.reset_cache()

    def initialize_cache(self, method_name: MethodNames,
                         llm_response: Union[
                             str, List[str], List[AIMessageChunk], List[BaseMessageChunk], BaseMessage, List[
                                 BaseMessageChunk]], *args: Any, **kwargs: Any):
        # convert llm response to message
        if isinstance(llm_response, str):
            message = AIMessage(content=llm_response)
        elif isinstance(llm_response, list):
            message = []
            for item in llm_response:
                if isinstance(item, str):
                    message.append(AIMessageChunk(content=item))
                elif isinstance(item, AIMessageChunk):
                    message.append(item)
                elif isinstance(item, BaseMessageChunk):
                    _dict = convert_ai_message_to_dict(item)
                    if "type" in _dict:
                        del _dict['type']
                    message.append(
                        AIMessageChunk(**_dict)
                    )
                else:
                    raise ValueError(f"[Pytest] Unable to identify type of item in llm_response. Type: {type(item)}")
        elif isinstance(llm_response, AIMessage):
            message = llm_response
        elif isinstance(llm_response, BaseMessage):
            _dict = convert_ai_message_to_dict(llm_response)
            if "type" in _dict:
                del _dict['type']
            message = AIMessageChunk(**_dict)
        else:
            raise ValueError(f"[Pytest] Unable to identify type of llm_response. Type: {type(llm_response)}")
        self.save_as_cache(method_name, message, *args, **kwargs)
