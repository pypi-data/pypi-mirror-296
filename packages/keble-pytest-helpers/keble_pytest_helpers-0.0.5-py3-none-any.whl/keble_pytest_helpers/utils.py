import logging
from typing import Dict, Any

from langchain_core.messages import AIMessageChunk, AIMessage, BaseMessage, BaseMessageChunk

logger = logging.getLogger(__name__)


def convert_ai_message_to_dict(message_chunk: AIMessage | AIMessageChunk | BaseMessage | BaseMessageChunk) -> Dict[
    str, Any]:
    """
    Converts an AIMessageChunk to a dictionary representation for JSON.

    Args:
        message_chunk (AIMessageChunk): The AIMessageChunk object to convert.

    Returns:
        Dict[str, Any]: A dictionary representation of the AIMessageChunk object.
    """
    # Define a dictionary to store the representation
    message_chunk_dict = {
        # "content": message_chunk.content,  # Main content of the message chunk
        # "additional_kwargs": message_chunk.additional_kwargs or {},  # Handle potential None values
    }

    # Optionally include additional attributes if they exist
    consider_fields = ["chunk_id", "type", "metadata", "timestamp", "source", "message_id", "sender", "content",
                       "additional_kwargs"]  # You can also include any extra fields if they are present
    for key in consider_fields:
        if hasattr(message_chunk, key):
            message_chunk_dict[key] = getattr(message_chunk, key)

    return message_chunk_dict
