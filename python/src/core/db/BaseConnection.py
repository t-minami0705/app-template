from abc import ABC, abstractmethod

class BaseConnection(ABC):
    """
    Base Class for Database Connection Management
    """
    def __init__(self):
        self._connection = None

    @abstractmethod
    def connect(self) -> None:
        """ Connect to the database """
        pass

    def close(self) -> None:
        """ Disconnection to the database """
        if self._connection:
            self._connection.close()
            self._connection = None

    def commit(self) -> None:
        """ Transaction commit """
        if self._connection:
            self._connection.commit()

    def rollback(self) -> None:
        if self._connection:
            self._connection.rollback()

    @property
    def is_connected(self) -> bool:
        """ Connection Status """
        return self._connection is not None
