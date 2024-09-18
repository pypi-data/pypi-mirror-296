from enum import Enum
from random import random as _random

from pyqrbtf.utils.center_module import CenterModule
from .utils.type_table import get_type_table, QRPointType


class ContentPointType(str, Enum):
    square = "square"
    circle = "circle"


def rand(start: float, end: float) -> float:
    return start + (end - start) * _random()


class DotsDrawer(CenterModule):
    def __init__(
        self,
        content_point_type: ContentPointType,
        content_point_scale: int = 0,
        content_point_opacity: int = 1,
        **kwargs,
    ):
        self.content_point_type = content_point_type

        self.content_point_scale = content_point_scale
        self.content_point_opacity = content_point_opacity
        super().__init__(**kwargs)

    def draw(self, matrix, colors):
        type_table = get_type_table(matrix)

        points = []

        content_point_size = self.content_point_scale * 1.01
        content_point_size_half = content_point_size / 2.0
        content_point_offset = (1 - content_point_size) / 2.0

        rect = self.rect
        circle = self.circle

        for y in range(len(matrix)):
            for x in range(len(matrix)):
                if not matrix[x][y]:
                    continue
                match type_table[x][y]:
                    case QRPointType.POS_OTHER:
                        continue
                    case QRPointType.POS_CENTER:
                        self.draw_center(points, colors, x, y)
                    case _:
                        color = colors.get(
                            type_table[x][y], colors.get(QRPointType.DATA, "#000")
                        )
                        is_constant = content_point_size > 0
                        if self.content_point_type == ContentPointType.square:
                            size = is_constant if content_point_size else rand(0.3, 1)
                            offset = (
                                is_constant
                                if content_point_offset
                                else (1 - size) / 2.0
                            )
                            points.append(
                                rect(
                                    opacity=self.content_point_opacity,
                                    width=size,
                                    height=size,
                                    fill=color,
                                    x=x + offset,
                                    y=y + offset,
                                ),
                            )
                        elif self.content_point_type == ContentPointType.circle:
                            half_size = (
                                is_constant
                                if content_point_size_half
                                else rand(0.3, 1) / 2.0
                            )
                            points.append(
                                circle(
                                    opacity=self.content_point_opacity,
                                    r=half_size,
                                    fill=color,
                                    cx=x + 0.5,
                                    cy=y + 0.5,
                                ),
                            )
        return points
