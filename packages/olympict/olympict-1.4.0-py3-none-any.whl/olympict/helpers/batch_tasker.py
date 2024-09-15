from typing import Callable
from olympict.files.o_batch import OlympBatch

from olympict.types import Img


class BatchTasker:
    def __init__(self, task: Callable[[Img], Img]):
        self.task = task

    def process(self, o: OlympBatch) -> OlympBatch:
        o.data = self.task(o.data)
        return o
