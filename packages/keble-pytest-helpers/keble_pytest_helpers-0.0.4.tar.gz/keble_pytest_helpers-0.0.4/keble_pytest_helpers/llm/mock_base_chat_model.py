from typing import List, Optional

from langchain_core.messages import AIMessage, AIMessageChunk

class MockBaseChatModel:

    def __init__(self, *, content: Optional[str] = None, streaming_contents: Optional[List[str]] = None):
        self.content = content
        self.streaming_contents = streaming_contents

    def invoke(self, *args, **kwargs):
        if self.content is not None:
            return AIMessage(content=self.content)
        return AIMessage(content="mock response")

    def stream(self, *args, **kwargs):
        if self.streaming_contents is not None:
            for content in self.streaming_contents:
                yield AIMessageChunk(content=content)
        else:
            yield AIMessageChunk(content="stream response 1")
            yield AIMessageChunk(content="stream response 2")

    async def astream(self, *args, **kwargs):
        if self.streaming_contents is not None:
            for content in self.streaming_contents:
                yield AIMessageChunk(content=content)
        else:
            yield AIMessageChunk(content="async stream response 1")
            yield AIMessageChunk(content="async stream response 2")

    async def ainvoke(self, *args, **kwargs):
        if self.content is not None:
            return AIMessage(content=self.content)
        return AIMessage(content="async mock response")
