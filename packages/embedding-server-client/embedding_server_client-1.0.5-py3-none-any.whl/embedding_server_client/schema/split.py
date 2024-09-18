from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from uuid import UUID

from embedding_server_client.schema import Embedding
from embedding_server_client.schema.summary import Summary
from embedding_server_client.schema.base import Base
from embedding_server_client.schema.document import RetrievalStatus


@dataclass
class Split(Base):
    """
    Dataclass representing a Split response.
    """
    split_id: int
    sequence_id: int
    doc_id: int
    text_content: str
    token_len: int
    summaries: List[Summary]


@dataclass
class SplitRetrievalRequest(Base):
    """
    Dataclass representing a split retrieval request.
    """
    split_id: int
    user: Optional[UUID] = field(default=None)
    verbose: Optional[bool] = field(default=False)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class SplitRetrievalResponse(Base):
    """
    Dataclass representing a split retrieval response.
    """
    status: RetrievalStatus
    split: Optional[Split] = field(default=None)
    embeddings: Optional[List[Embedding]] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "status": RetrievalStatus,
        }
