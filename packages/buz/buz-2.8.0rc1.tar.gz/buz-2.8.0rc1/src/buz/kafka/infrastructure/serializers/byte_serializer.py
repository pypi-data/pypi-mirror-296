from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class ByteSerializer(ABC, Generic[T]):
    @abstractmethod
    def serialize(self, data: T) -> bytes:
        pass

    @abstractmethod
    def unserialize(self, data: bytes) -> T:
        pass
