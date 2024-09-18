from enum import Enum


class DocumentInsertionStatus(Enum):
    """
    Enum that represent the insertion status of the Document.
    """
    SUCCESS = 1
    ERROR = 2


class RetrievalStatus(Enum):
    """
    Enum that represent the retrieval status of the Document.
    """
    SUCCESS = 1
    NOTFOUND = 2
    ERROR = 3


class DeletionStatus(Enum):
    """
    Enum that represent the deletion status of the Document.
    """
    SUCCESS = 1
    NOTFOUND = 2
    ERROR = 3
