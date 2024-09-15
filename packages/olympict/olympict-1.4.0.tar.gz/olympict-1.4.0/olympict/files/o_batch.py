from typing import Any, Dict, List, Optional

import numpy as np

from olympict.files.o_file import OlympFile
from olympict.files.o_image import OlympImage
from olympict.types import Img, Size


class OlympBatch(OlympFile):
    def __init__(
        self,
        data: Img,
        paths: Optional[List[str]] = None,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ):
        assert len(data.shape) >= 4
        self.data = data
        self.paths = paths or []
        self.metadata = metadata or []

    @property
    def size(self) -> Size:
        _, h, w, _ = self.data.shape
        return (w, h)

    @staticmethod
    def from_images(images: List[OlympImage]) -> "OlympBatch":
        data = np.array([i.img for i in images])
        paths = [i.path for i in images]
        metadata = [i.metadata for i in images]

        return OlympBatch(
            data,
            paths,
            metadata,
        )

    @staticmethod
    def to_images(batch: "OlympBatch") -> List[OlympImage]:
        out = [
            OlympImage.from_buffer(
                batch.data[i, :, :, :], batch.paths[i], batch.metadata[i]
            )
            for i in range(batch.data.shape[0])
        ]
        return out
