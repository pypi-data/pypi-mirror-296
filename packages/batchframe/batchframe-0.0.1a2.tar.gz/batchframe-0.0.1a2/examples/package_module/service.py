from kink import inject
from batchframe import Service, Source
import asyncio
from .config.custom_configuration import CustomConfigExample
from .source import TestSource # Important for DI discovery!
import logging

@inject()
class AnotherService(Service):

    source: Source
    _exceptions_to_retry_for = {ValueError}

    def __init__(self, source: Source, config: CustomConfigExample) -> None:
        self.source = source

    def name(self):
        return "brat"
    
    @property
    def exceptions_to_retry_for(self) -> set[type[Exception]]:
        return self._exceptions_to_retry_for

    async def process(self, input):
        await asyncio.sleep(1)
        if input == 'Item 5':
            raise ValueError("Fake exception")
    
    def finish(self):
        logging.info("finish() called! Pretending to do work...")