from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from uuid import UUID

from embedding_server_client.schema.embedding import Embedding
from embedding_server_client.schema.base import Base
from embedding_server_client.schema.document import RetrievalStatus


@dataclass
class Summary(Base):
    """
    Dataclass representing a Summary response.
    """
    summary_id: int
    document_id: int
    split_id: int
    split_sequence_id: int
    text_content: str
    token_len: int
    tokens: Optional[List[int]]


@dataclass
class SummaryRetrievalRequest(Base):
    """
    Dataclass representing a summary retrieval request.
    """
    summary_id: int
    user: Optional[UUID] = field(default=None)
    verbose: Optional[bool] = field(default=False)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class SummaryRetrievalResponse(Base):
    """
    Dataclass representing a summary retrieval response.
    """
    status: RetrievalStatus
    summary: Optional[Summary] = field(default=None)
    embeddings: Optional[List[Embedding]] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "status": RetrievalStatus,
        }
