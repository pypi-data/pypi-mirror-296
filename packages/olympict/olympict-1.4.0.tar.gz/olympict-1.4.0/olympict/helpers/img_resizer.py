from olympict.files.o_image import OlympImage
from olympict.image_tools import ImTools
from olympict.types import Size, Color
import cv2
from typing import Optional
import numpy as np


class Resizer:
    def __init__(
        self,
        size: Size,
        pad_color: Optional[Color] = None,
        interpolation: int = cv2.INTER_LINEAR,
    ):
        self.size = size
        self.pad_color = pad_color
        self.interpolation = interpolation

    def process(self, o: OlympImage) -> OlympImage:
        if self.pad_color is None:
            o.img = cv2.resize(
                o.img.astype(np.uint8), self.size, interpolation=self.interpolation
            )
        else:
            o.img = ImTools.pad_to_output_size(
                o.img, self.size, self.pad_color, interpolation=self.interpolation
            )
        return o
