import uuid
import pytest

from embedding_server_client.client import EmbeddingClient
from embedding_server_client.schema import (
    DocumentInsertionRequest,
    DocumentInsertionResponse,
    DocumentQueryRequest,
    DocumentQueryResponse)

HOST = "tcp://localhost:5556"

@pytest.fixture
def bert_client():
    host = HOST
    client = EmbeddingClient(host)
    yield client
    client.close()
    
def test_index_request_file_turkish(bert_client):
    file_path = "data/telekomturkishsample.txt"
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
