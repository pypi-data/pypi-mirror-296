from kink import inject
from batchframe import Source, BatchframeParam
import logging

@inject()
class TestSource(Source[str]):

    _curr_count = 0
    _total_items = 25

    def name(self):
        return "SourceName"

    def __init__(self, test_param: BatchframeParam[str]) -> None:
        logging.debug(f'Source got {test_param=}')

    def __iter__(self):
        return self
    
    def __next__(self) -> str:
        return self.next()
    
    def __len__(self) -> int:
        return self._total_items
    
    def next(self) -> str:
        self._curr_count += 1
        if self._curr_count <= self._total_items:
            return f"Item {self._curr_count}"
        else:
            raise StopIteration()

    def persist_failed(self, failed: list[str]):
        logging.debug(f"Persisting failed inputs: {failed}")