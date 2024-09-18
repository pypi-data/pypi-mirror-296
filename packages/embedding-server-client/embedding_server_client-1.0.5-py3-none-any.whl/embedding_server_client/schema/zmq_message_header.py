import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID

from embedding_server_client.schema import SummaryRetrievalResponse
from embedding_server_client.schema.base import Base
from embedding_server_client.schema.document import (
    DocumentInsertionResponse,
    DocumentQueryResponse,
    DocumentRetrievalResponse,
    DocumentSplitsRetrievalResponse, DocumentSummariesRetrievalResponse,
    DocumentDeletionResponse
)
from embedding_server_client.schema.health_check import HealthCheck
from embedding_server_client.schema.split import SplitRetrievalResponse


class ZmqMessageType(Enum):
    """
    ZmqMessageType defines the types of messages used in a ZeroMQ messaging system.
    Each type is associated with a specific class for handling its data.
    """
    DOCUMENT_INSERTION = 1
    DOCUMENT_QUERY = 2
    DOCUMENT_RETRIEVAL = 3
    DOCUMENT_SPLITS_RETRIEVAL = 4
    DOCUMENT_SUMMARIES_RETRIEVAL = 5
    DOCUMENT_DELETION = 6
    SPLIT_RETRIEVAL = 7
    SUMMARY_RETRIEVAL = 8
    HEALTH_CHECK = 9
    UNKNOWN = 10

    @property
    def get_associated_class(self):
        return {
            ZmqMessageType.DOCUMENT_INSERTION: DocumentInsertionResponse,
            ZmqMessageType.DOCUMENT_QUERY: DocumentQueryResponse,
            ZmqMessageType.DOCUMENT_RETRIEVAL: DocumentRetrievalResponse,
            ZmqMessageType.DOCUMENT_SPLITS_RETRIEVAL: DocumentSplitsRetrievalResponse,
            ZmqMessageType.DOCUMENT_SUMMARIES_RETRIEVAL: DocumentSummariesRetrievalResponse,
            ZmqMessageType.DOCUMENT_DELETION: DocumentDeletionResponse,
            ZmqMessageType.SPLIT_RETRIEVAL: SplitRetrievalResponse,
            ZmqMessageType.SUMMARY_RETRIEVAL: SummaryRetrievalResponse,
            ZmqMessageType.HEALTH_CHECK: HealthCheck,
            ZmqMessageType.UNKNOWN: lambda x: None,
        }.get(self, lambda x: None)


class ZmqMessageStatus(Enum):
    """
    ZmqMessageStatus is an enumeration representing the status of a ZeroMQ message.
    It indicates whether a message was processed successfully or encountered an error.
    """
    SUCCESS = 1
    ERROR = 2


@dataclass
class ZmqMessageHeader(Base):
    """
    ZmqMessageHeader represents the header information of a ZeroMQ message.
    It contains essential data like message ID, type, status, and timestamps.
    """
    zmq_message_id: UUID
    message_type: ZmqMessageType
    status: Optional[ZmqMessageStatus] = None
    error_code: Optional[int] = None
    error_message: Optional[str] = None
    request_ts: Optional[datetime] = None
    response_ts: Optional[datetime] = None

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        """
        Provides a mapping for decoding the fields of a ZmqMessageHeader.

        :return: A dictionary where keys are field names and values are their corresponding data types.
        """
        return {
            "zmq_message_id": UUID,
            "message_type": ZmqMessageType,
            "status": ZmqMessageStatus,
            "request_ts": datetime,
            "response_ts": datetime,
        }


def create_message_header(message_type: ZmqMessageType) -> ZmqMessageHeader:
    """
    Creates and returns a new ZmqMessageHeader with a unique ID and the current timestamp.

    :param message_type: The type of the ZeroMQ message.
    :return: An instance of ZmqMessageHeader with the specified message type and other default values.
    """
    return ZmqMessageHeader(
        zmq_message_id=uuid.uuid4(),
        message_type=message_type,
        request_ts=datetime.now()
    )
