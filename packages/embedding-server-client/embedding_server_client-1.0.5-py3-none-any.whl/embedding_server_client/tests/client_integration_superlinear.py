import uuid
from concurrent.futures import ThreadPoolExecutor
import pytest

from embedding_server_client.client import EmbeddingClient
from embedding_server_client.schema import (
    DocumentInsertionRequest,
    DocumentInsertionResponse,
    DocumentQueryRequest,
    DocumentQueryResponse)
from embedding_server_client.schema.document import DocumentSummariesRetrievalRequest, DocumentSummariesRetrievalResponse

HOST = "tcp://localhost:5556"

@pytest.fixture
def bert_client():
    host = HOST
    client = EmbeddingClient(host)
    yield client
    client.close()


def test_index_request_file_superlinear(bert_client):
    file_path = "test_data/superlinear.txt"
    with open(file_path, 'r') as file:
        content = file.read()

    request = DocumentInsertionRequest(
        input=[content],
        model="test_model",
        user=uuid.uuid4(),
        doc_urls=[file_path],
        verbose=True)
    response = bert_client.send_document_insertion_request(request)

    assert response is not None
    assert isinstance(response, DocumentInsertionResponse)
    print(response.to_json_str(indent=4))

def test_query_request_file_superlinear(bert_client):
    request = DocumentQueryRequest(
        input="How can I avoid going out of business?",
        model="test_model", user=uuid.uuid4(),
        top_k=3)
    response = bert_client.send_query_request(request)

    assert response is not None
    assert isinstance(response, DocumentQueryResponse)
    print(response.to_json_str(indent=4))


def test_document_summaries_retrieval(bert_client):
    request = DocumentSummariesRetrievalRequest(
        document_id=7539349182657362181
    )
    response = bert_client.send_document_summaries_retrieval_request(request)

    assert response is not None
    assert isinstance(response, DocumentSummariesRetrievalResponse)
    print(response.to_json_str(indent=4))
