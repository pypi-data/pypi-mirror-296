from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Source(Generic[T], metaclass=ABCMeta):
    
    def __iter__(self):
        return self
    
    def __next__(self) -> T:
        return self.next()
    
    @abstractmethod
    def __len__(self) -> int:
        pass
    
    @abstractmethod
    def next(self) -> T:
        pass

    @abstractmethod
    def persist_failed(self, failed: list[T]):
        pass