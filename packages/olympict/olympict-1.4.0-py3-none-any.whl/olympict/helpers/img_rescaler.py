from typing import Tuple, Optional

import numpy as np
from olympict.files.o_image import Color, OlympImage
import cv2

from olympict.image_tools import ImTools


class ImgRescaler:
    """Rescale class
    This class applies a scale [x_s, y_s] to a given image
    The resulting image dimensions are [w * x_s, h * y_s]
    """

    def __init__(
        self,
        scales: Tuple[float, float],
        pad_color: Optional[Color] = None,
        interpolation: int = cv2.INTER_LINEAR,
    ):
        self.scales = scales
        self.pad_color = pad_color
        self.interpolation = interpolation

    def process(self, o: OlympImage) -> OlympImage:
        w, h = o.size
        x_scale, y_scale = self.scales
        size = (int(round(w * x_scale)), int(round(h * y_scale)))
        if self.pad_color is None:
            o.img = cv2.resize(
                o.img.astype(np.uint8), size, interpolation=self.interpolation
            )
        else:
            o.img = ImTools.pad_to_output_size(
                o.img, size, self.pad_color, interpolation=self.interpolation
            )
        return o
