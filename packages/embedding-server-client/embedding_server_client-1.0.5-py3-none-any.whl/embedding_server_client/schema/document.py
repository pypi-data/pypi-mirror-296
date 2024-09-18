from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any
from uuid import UUID

from embedding_server_client.schema.embedding import Embedding, EmbeddingUsage
from embedding_server_client.schema.document_status import DocumentInsertionStatus, RetrievalStatus, DeletionStatus
from embedding_server_client.schema.summary import Summary
from embedding_server_client.schema.base import Base
from embedding_server_client.schema.split import Split


@dataclass
class Document(Base):
    """
    Dataclass representing a Document response.
    """
    document_id: int
    document_url: str
    splits: List[Split]
    summaries: List[Summary]


@dataclass
class DocumentInsertionRequest(Base):
    """
    Dataclass representing a document insertion request.
    """
    input: Union[str, List[str]]
    model: str
    user: Optional[UUID] = field(default=None)
    doc_urls: Optional[Union[str, List[str]]] = field(default=None)
    verbose: Optional[bool] = field(default=False)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class DocumentInsertionResponse(Base):
    """
    Dataclass representing a document insertion response.
    """
    status: DocumentInsertionStatus
    documents: Optional[List[Document]] = field(default=None)
    embeddings: Optional[List[Embedding]] = field(default=None)
    usage: Optional[EmbeddingUsage] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "status": DocumentInsertionStatus,
        }


@dataclass
class DocumentRetrievalRequest(Base):
    """
    Dataclass representing a document retrieval request.
    """
    document_id: Optional[int] = field(default=None)
    document_url: Optional[str] = field(default=None)
    user: Optional[UUID] = field(default=None)
    verbose: Optional[bool] = field(default=False)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class DocumentRetrievalResponse(Base):
    """
    Dataclass representing a document retrieval response.
    """
    status: RetrievalStatus
    document: Optional[Document] = field(default=None)
    embeddings: Optional[List[Embedding]] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "status": RetrievalStatus,
        }


@dataclass
class DocumentQueryRequest(Base):
    """
    Dataclass representing a document query request.
    """
    input: str
    model: str
    top_k: Optional[int] = field(default=5)
    encoding_format: Optional[str] = field(default="float")
    dimensions: Optional[int] = field(default=None)
    user: Optional[UUID] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class DocumentQueryResponse(Base):
    """
    Dataclass representing a document query response.
    """
    documents: List[Document]
    model: Optional[str] = field(default=None)
    usage: Optional[EmbeddingUsage] = field(default=None)


@dataclass
class DocumentSplitsRetrievalRequest(Base):
    """
    Dataclass representing splits of a document retrieval request.
    """
    document_id: int = field(default=None)
    user: Optional[UUID] = field(default=None)
    verbose: Optional[bool] = field(default=False)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class DocumentSplitsRetrievalResponse(Base):
    """
    Dataclass representing splits of document retrieval response.
    """
    status: RetrievalStatus
    document_id: int
    document_url: str
    splits: Optional[List[Split]] = field(default=None)
    embeddings: Optional[List[List[Embedding]]] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "status": RetrievalStatus,
        }


@dataclass
class DocumentSummariesRetrievalRequest(Base):
    """
    Dataclass representing summaries of a document retrieval request.
    """
    document_id: int = field(default=None)
    user: Optional[UUID] = field(default=None)
    verbose: Optional[bool] = field(default=False)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class DocumentSummariesRetrievalResponse(Base):
    """
    Dataclass representing summaries of document retrieval response.
    """
    status: RetrievalStatus
    document_id: int
    document_url: str
    summaries: Optional[List[Summary]] = field(default=None)
    embeddings: Optional[List[List[Embedding]]] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "status": RetrievalStatus,
        }


@dataclass
class DocumentDeletionRequest(Base):
    """
    Dataclass representing a request for deleting a document.
    """
    document_id: int = field(default=None)
    user: Optional[UUID] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class DocumentDeletionResponse(Base):
    """
    Dataclass representing summaries of document retrieval response.
    """
    status: DeletionStatus

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "status": DeletionStatus,
        }
