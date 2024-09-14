from kink import inject
from batchframe import Service, Source, BatchframeParam
import asyncio
import logging

@inject()
class TestSource(Source[str]):

    _curr_count = 0

    def name(self):
        return "SourceName"

    def __init__(self, test_param: BatchframeParam[str]) -> None:
        logging.debug(f'Source got {test_param=}')

    def __iter__(self):
        return self
    
    def __next__(self) -> str:
        return self.next()
    
    def __len__(self) -> int:
        return 10
    
    def next(self) -> str:
        self._curr_count += 1
        if self._curr_count <= 10:
            return f"Item {self._curr_count}"
        else:
            raise StopIteration()

    def persist_failed(self, failed: list[str]):
        logging.debug(f"Persisting failed inputs: {failed}")

@inject()
class AnotherService(Service):

    source: TestSource
    _exceptions_to_retry_for = {ValueError}

    def name(self):
        return "brat"
    
    @property
    def exceptions_to_retry_for(self) -> set[type[Exception]]:
        return self._exceptions_to_retry_for

    def __init__(self, source: TestSource) -> None:
        self.source = source

    async def process(self, input):
        await asyncio.sleep(1)
        if input == 'Item 5':
            raise ValueError("Fake exception")
        
    def finish(self):
        logging.debug("Finish called!")
