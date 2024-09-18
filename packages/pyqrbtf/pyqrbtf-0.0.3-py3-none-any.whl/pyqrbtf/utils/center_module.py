from enum import Enum

from .base_drawer import BaseDrawer
from .const import sq25
from .type_table import QRPointType


class PositioningPointType(str, Enum):
    square = "square"
    circle = "circle"
    planet = "planet"
    rounded = "rounded"
    dsj = "dsj"


class CenterModule(BaseDrawer):
    def __init__(
        self,
        positioning_point_type: PositioningPointType,
        positioning_stroke_width=0.8,
        **kwargs,
    ):
        self.positioning_stroke_width = positioning_stroke_width
        self.positioning_point_type = positioning_point_type
        super().__init__(**kwargs)

    def draw_center(self, points, colors, x, y):
        color_center = colors.get(
            QRPointType.POS_CENTER, colors.get(QRPointType.DATA, "#000")
        )
        color_other = colors.get(
            QRPointType.POS_OTHER,
            colors.get(QRPointType.POS_CENTER, colors.get(QRPointType.DATA, "#000")),
        )

        vw = [3, -3]
        vh = [3, -3]

        if self.positioning_point_type == PositioningPointType.square:
            points.append(
                self.rect(
                    fill=color_center,
                    x=x + 0.5 - 1.5,
                    y=y + 0.5 - 1.5,
                    width=3,
                    height=3,
                ),
            )
            points.append(
                self.rect(
                    fill="none",
                    stroke_width=self.positioning_stroke_width,
                    stroke=color_other,
                    x=x + 0.5 - 3,
                    y=y + 0.5 - 3,
                    width=6,
                    height=6,
                ),
            )
        elif self.positioning_point_type == PositioningPointType.circle:
            points.append(
                self.circle(
                    fill=color_center,
                    cx=x + 0.5,
                    cy=y + 0.5,
                    r=1.5,
                ),
            )
            points.append(
                self.circle(
                    fill="none",
                    stroke_width=self.positioning_stroke_width,
                    stroke=color_other,
                    cx=x + 0.5,
                    cy=y + 0.5,
                    r=3,
                ),
            )
        elif self.positioning_point_type == PositioningPointType.planet:
            points.append(
                self.circle(
                    fill=color_center,
                    cx=x + 0.5,
                    cy=y + 0.5,
                    r=1.5,
                ),
            )
            points.append(
                self.circle(
                    fill="none",
                    stroke_width="0.15",
                    stroke_dasharray="0.5,0.5",
                    stroke=color_other,
                    cx=x + 0.5,
                    cy=y + 0.5,
                    r=3,
                ),
            )
            for w in range(len(vw)):
                points.append(
                    self.circle(
                        fill=color_other,
                        cx=x + vw[w] + 0.5,
                        cy=y + 0.5,
                        r=self.positioning_stroke_width,
                    ),
                )
            for h in range(len(vh)):
                points.append(
                    self.circle(
                        fill=color_other,
                        cx=x + 0.5,
                        cy=y + vh[h] + 0.5,
                        r=self.positioning_stroke_width,
                    ),
                )
        elif self.positioning_point_type == PositioningPointType.rounded:
            points.append(
                self.circle(
                    fill=color_center,
                    cx=x + 0.5,
                    cy=y + 0.5,
                    r=1.5,
                ),
            )
            points.append(
                self.path(
                    d=sq25,
                    stroke=color_other,
                    stroke_width=(100 / 6.0)
                    * (1 - (1 - self.positioning_stroke_width) * 0.75),
                    fill="none",
                    transform=f"translate({x - 2.5} ,{y - 2.5}) scale({6 / 100.} ,{6 / 100.})",
                ),
            )

        elif self.positioning_point_type == PositioningPointType.dsj:
            points.append(
                self.rect(
                    width=3 - (1 - self.positioning_stroke_width),
                    height=3 - (1 - self.positioning_stroke_width),
                    fill=color_center,
                    x=x - 1 + (1 - self.positioning_stroke_width) / 2.0,
                    y=y - 1 + (1 - self.positioning_stroke_width) / 2.0,
                ),
            )
            points.append(
                self.rect(
                    width=self.positioning_stroke_width,
                    height=3 - (1 - self.positioning_stroke_width),
                    fill=color_other,
                    x=x - 3 + (1 - self.positioning_stroke_width) / 2.0,
                    y=y - 1 + (1 - self.positioning_stroke_width) / 2.0,
                ),
            )
            points.append(
                self.rect(
                    width=self.positioning_stroke_width,
                    height=3 - (1 - self.positioning_stroke_width),
                    fill=color_other,
                    x=x + 3 + (1 - self.positioning_stroke_width) / 2.0,
                    y=y - 1 + (1 - self.positioning_stroke_width) / 2.0,
                ),
            )
            points.append(
                self.rect(
                    width=3 - (1 - self.positioning_stroke_width),
                    height=self.positioning_stroke_width,
                    fill=color_other,
                    x=x - 1 + (1 - self.positioning_stroke_width) / 2.0,
                    y=y - 3 + (1 - self.positioning_stroke_width) / 2.0,
                ),
            )
            points.append(
                self.rect(
                    width=3 - (1 - self.positioning_stroke_width),
                    height=self.positioning_stroke_width,
                    fill=color_other,
                    x=x - 1 + (1 - self.positioning_stroke_width) / 2.0,
                    y=y + 3 + (1 - self.positioning_stroke_width) / 2.0,
                ),
            )
