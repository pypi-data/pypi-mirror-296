import zmq
from typing import Optional, List, Type

from embedding_server_client.error import EmbeddingClientError
from embedding_server_client.schema.base import T
from embedding_server_client.schema.document import (
    DocumentInsertionRequest,
    DocumentQueryRequest,
    DocumentQueryResponse,
    DocumentInsertionResponse,
    DocumentRetrievalRequest,
    DocumentRetrievalResponse,
    DocumentSplitsRetrievalRequest,
    DocumentSplitsRetrievalResponse,
    DocumentSummariesRetrievalRequest,
    DocumentSummariesRetrievalResponse,
    DocumentDeletionRequest,
    DocumentDeletionResponse,
)
from embedding_server_client.schema.health_check import HealthCheck
from embedding_server_client.schema.split import SplitRetrievalRequest, SplitRetrievalResponse
from embedding_server_client.schema.summary import SummaryRetrievalRequest, SummaryRetrievalResponse
from embedding_server_client.schema.zmq_message_header import (
    ZmqMessageHeader,
    create_message_header,
    ZmqMessageStatus,
    ZmqMessageType,
)


class EmbeddingClient:
    def __init__(self, host: str, timeout: int = 360000) -> None:
        """
        Initializes a new instance of the EmbeddingClient.

        Args:
            host (str): The address of the server to connect to.
            timeout (int): Timeout for receiving a response in milliseconds.
        """
        self.host: str = host
        self.timeout: int = timeout
        self.context: Optional[zmq.Context] = None
        self.socket: Optional[zmq.Socket] = None
        self.initialize_client()

    def __del__(self) -> None:
        """
        Destructor to ensure proper cleanup. It's called when the instance is being destroyed.
        """
        self.close()

    def initialize_client(self) -> None:
        """
        Sets up the ZMQ context and socket for communication with the server.
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.socket.connect(self.host)

    def close(self) -> None:
        """
        Closes the ZMQ socket and terminates the context, releasing any system resources used.
        """
        if self.socket:
            self.socket.close()
        if self.context:
            self.context.term()

    def _send_request(self, zmq_message_type: ZmqMessageType, request: Optional[T] = None) -> Optional[T]:
        """
        Sends a request to the server, according to the specified message type, and waits for a response.

        Args:
            zmq_message_type (ZmqMessageType): The type of the ZeroMQ message to be sent.
            request (Optional[T]): The request object to be sent, if applicable.

        Returns:
            Optional[T]: The unpacked response if successful, or raises an exception.

        Raises:
            Exception: For any network-related errors or data packing/unpacking issues.
        """
        message_header: ZmqMessageHeader = create_message_header(zmq_message_type)
        message_parts: List[bytes] = [message_header.msgpack_pack()]
        if request:
            message_parts.append(request.msgpack_pack())

        self.socket.send_multipart(message_parts)

        try:
            resp_messages: List[bytes] = self.socket.recv_multipart()
            if len(resp_messages) > 2:
                raise ValueError("Invalid response length")

            response_header: ZmqMessageHeader = ZmqMessageHeader.msgpack_unpack(resp_messages[0])
            if response_header.status == ZmqMessageStatus.ERROR:
                raise EmbeddingClientError(response_header)

            response_body_cls: Type[T] = zmq_message_type.get_associated_class
            return response_body_cls.msgpack_unpack(resp_messages[1])
        except Exception as e:
            self.initialize_client()
            raise e

    def send_document_insertion_request(self, request: DocumentInsertionRequest) -> Optional[DocumentInsertionResponse]:
        """
        Sends a document insertion request to the server and waits for a response.

        Args:
            request (DocumentInsertionRequest): The request object containing the data for embedding and insertion
            into the vector DB.

        Returns:
            Optional[DocumentInsertionResponse]: The response from the server.

        Raises:
            ValueError: If the provided request is not of type DocumentInsertionRequest.
        """
        if not isinstance(request, DocumentInsertionRequest):
            raise ValueError("Invalid request type provided")

        if isinstance(request.input, str):
            request.input = [request.input]

        if isinstance(request.doc_urls, str):
            request.doc_urls = [request.doc_urls]

        return self._send_request(ZmqMessageType.DOCUMENT_INSERTION, request)

    def send_document_retrieval_request(self, request: DocumentRetrievalRequest) -> Optional[DocumentRetrievalResponse]:
        """
        Sends a document retrieval request to the server and waits for a response.

        Args:
            request (DocumentRetrievalRequest): The request object containing the document_id or document_url.

        Returns:
            Optional[DocumentRetrievalResponse]: The response from the server.

        Raises:
            ValueError: If the provided request is not of type DocumentRetrievalRequest.
        """
        if not isinstance(request, DocumentRetrievalRequest):
            raise ValueError("Invalid request type provided")

        return self._send_request(ZmqMessageType.DOCUMENT_RETRIEVAL, request)

    def send_document_splits_retrieval_request(
            self,
            request: DocumentSplitsRetrievalRequest
    ) -> Optional[DocumentSplitsRetrievalResponse]:
        """
        Sends a document splits retrieval request to the server and waits for a response.

        Args:
            request (DocumentSplitsRetrievalRequest): The request object containing the document_id.

        Returns:
            Optional[DocumentSplitsRetrievalResponse]: The response from the server.

        Raises:
            ValueError: If the provided request is not of type DocumentRetrievalRequest.
        """
        if not isinstance(request, DocumentSplitsRetrievalRequest):
            raise ValueError("Invalid request type provided")

        return self._send_request(ZmqMessageType.DOCUMENT_SPLITS_RETRIEVAL, request)

    def send_document_summaries_retrieval_request(
            self,
            request: DocumentSummariesRetrievalRequest
    ) -> Optional[DocumentSummariesRetrievalResponse]:
        """
        Sends a document summaries retrieval request to the server and waits for a response.

        Args:
            request (DocumentSummariesRetrievalRequest): The request object containing the document_id.

        Returns:
            Optional[DocumentSummariesRetrievalResponse]: The response from the server.

        Raises:
            ValueError: If the provided request is not of type DocumentRetrievalRequest.
        """
        if not isinstance(request, DocumentSummariesRetrievalRequest):
            raise ValueError("Invalid request type provided")

        return self._send_request(ZmqMessageType.DOCUMENT_SUMMARIES_RETRIEVAL, request)

    def send_query_request(self, request: DocumentQueryRequest) -> Optional[DocumentQueryResponse]:
        """
        Sends a query request to the server and waits for a response.

        Args:
            request (DocumentQueryRequest): The request object containing the query data.

        Returns:
            Optional[DocumentQueryResponse]: The response from the server.

        Raises:
            ValueError: If the provided request is not of type DocumentQueryRequest.
        """
        if not isinstance(request, DocumentQueryRequest):
            raise ValueError("Invalid request type provided")

        return self._send_request(ZmqMessageType.DOCUMENT_QUERY, request)

    def send_split_retrieval_request(self, request: SplitRetrievalRequest) -> Optional[SplitRetrievalResponse]:
        """
        Sends a split retrieval request to the server and waits for a response.

        Args:
            request (SplitRetrievalRequest): The request object containing the split_id.

        Returns:
            Optional[SplitRetrievalResponse]: The response from the server.

        Raises:
            ValueError: If the provided request is not of type SplitRetrievalRequest.
        """
        if not isinstance(request, SplitRetrievalRequest):
            raise ValueError("Invalid request type provided")

        return self._send_request(ZmqMessageType.SPLIT_RETRIEVAL, request)

    def send_summary_retrieval_request(self, request: SummaryRetrievalRequest) -> Optional[SummaryRetrievalResponse]:
        """
        Sends a summary retrieval request to the server and waits for a response.

        Args:
            request (SummaryRetrievalRequest): The request object containing the summary_id.

        Returns:
            Optional[SummaryRetrievalResponse]: The response from the server.

        Raises:
            ValueError: If the provided request is not of type SummaryRetrievalRequest.
        """
        if not isinstance(request, SummaryRetrievalRequest):
            raise ValueError("Invalid request type provided")

        return self._send_request(ZmqMessageType.SUMMARY_RETRIEVAL, request)

    def send_document_deletion_request(self, request: DocumentDeletionRequest) -> Optional[DocumentDeletionResponse]:
        """
        Sends a document deletion request to the server and waits for a response.

        Args:
            request (DocumentDeletionRequest): The request object containing the summary_id.

        Returns:
            Optional[DocumentDeletionResponse]: The response from the server.

        Raises:
            ValueError: If the provided request is not of type DocumentDeletionRequest.
        """
        if not isinstance(request, DocumentDeletionRequest):
            raise ValueError("Invalid request type provided")

        return self._send_request(ZmqMessageType.DOCUMENT_DELETION, request)

    def send_health_check_request(self) -> Optional[HealthCheck]:
        """
        Sends a HealthCheck request to the server and waits for a HealthCheck response.

        Returns:
            Optional[HealthCheck]: A HealthCheck response or None if timed out.
        """
        return self._send_request(ZmqMessageType.HEALTH_CHECK)
