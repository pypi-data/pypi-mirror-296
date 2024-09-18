from enum import Enum
from random import random as _random

from pyqrbtf.utils.center_module import CenterModule
from .utils.type_table import get_type_table, QRPointType


class ContentLineType(str, Enum):
    radial = "radial"
    horizontal = "horizontal"
    vertical = "vertical"
    tl_br = "tl_br"
    tr_bl = "tr_bl"
    cross = "cross"
    interlock = "interlock"


def random(start: float, end: float) -> float:
    return start + (end - start) * _random()


class LinesDrawer(CenterModule):
    def __init__(
        self,
        content_line_type: ContentLineType,
        content_point_scale=0.5,
        content_point_opacity=1,
        **kwargs,
    ):
        self.content_line_type = content_line_type

        self.content_point_scale = content_point_scale
        self.content_point_opacity = content_point_opacity
        super().__init__(**kwargs)

    def draw(self, matrix, colors):
        type_table = get_type_table(matrix)

        points = []

        n_count = len(matrix)

        opacity = self.content_point_opacity
        size = self.content_point_scale

        available = [[True] * n_count for _ in range(n_count)]
        ava2 = [[True] * n_count for _ in range(n_count)]

        line = self.line
        circle = self.circle

        for y in range(n_count):
            for x in range(n_count):
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
                        if self.content_line_type == ContentLineType.horizontal:
                            if x == 0 or (
                                x > 0 and (not matrix[x - 1][y] or not ava2[x - 1][y])
                            ):
                                start = 0
                                end = 0
                                ctn = True
                                while ctn and x + end < n_count:
                                    if matrix[x + end][y] and ava2[x + end][y]:
                                        end += 1
                                    else:
                                        ctn = False

                                if end - start > 1:
                                    for i in range(start, end):
                                        ava2[x + i][y] = False
                                        available[x + i][y] = False

                                    points.append(
                                        line(
                                            opacity=opacity,
                                            x1=x + 0.5,
                                            y1=y + 0.5,
                                            x2=x + end - start - 0.5,
                                            y2=y + 0.5,
                                            stroke_width=size,
                                            stroke=color,
                                            stroke_linecap="round",
                                        ),
                                    )

                            if available[x][y]:
                                points.append(
                                    circle(
                                        opacity=opacity,
                                        r=size / 2.0,
                                        fill=color,
                                        cx=x + 0.5,
                                        cy=y + 0.5,
                                    ),
                                )

                        if self.content_line_type == ContentLineType.vertical:
                            if y == 0 or (
                                y > 0 and (not matrix[x][y - 1] or not ava2[x][y - 1])
                            ):
                                start = 0
                                end = 0
                                ctn = True
                                while ctn and y + end < n_count:
                                    if matrix[x][y + end] and ava2[x][y + end]:
                                        end += 1
                                    else:
                                        ctn = False

                                if end - start > 1:
                                    for i in range(start, end):
                                        ava2[x][y + i] = False
                                        available[x][y + i] = False

                                    points.append(
                                        line(
                                            opacity=opacity,
                                            x1=x + 0.5,
                                            y1=y + 0.5,
                                            x2=x + 0.5,
                                            y2=y + end - start - 1 + 0.5,
                                            stroke_width=size,
                                            stroke=color,
                                            stroke_linecap="round",
                                        ),
                                    )

                            if available[x][y]:
                                points.append(
                                    circle(
                                        opacity=opacity,
                                        r=size / 2.0,
                                        fill=color,
                                        cx=x + 0.5,
                                        cy=y + 0.5,
                                    ),
                                )

                        if self.content_line_type == ContentLineType.interlock:
                            if y == 0 or (
                                y > 0 and (not matrix[x][y - 1] or not ava2[x][y - 1])
                            ):
                                start = 0
                                end = 0
                                ctn = True
                                while ctn and y + end < n_count:
                                    if (
                                        matrix[x][y + end]
                                        and ava2[x][y + end]
                                        and end - start <= 3
                                    ):
                                        end += 1
                                    else:
                                        ctn = False

                                if end - start > 1:
                                    for i in range(start, end):
                                        ava2[x][y + i] = False
                                        available[x][y + i] = False

                                    points.append(
                                        line(
                                            opacity=opacity,
                                            x1=x + 0.5,
                                            y1=y + 0.5,
                                            x2=x + 0.5,
                                            y2=y + end - start - 1 + 0.5,
                                            stroke_width=size,
                                            stroke=color,
                                            stroke_linecap="round",
                                        ),
                                    )

                            if x == 0 or (
                                x > 0 and (not matrix[x - 1][y] or not ava2[x - 1][y])
                            ):
                                start = 0
                                end = 0
                                ctn = True
                                while ctn and x + end < n_count:
                                    if (
                                        matrix[x + end][y]
                                        and ava2[x + end][y]
                                        and end - start <= 3
                                    ):
                                        end += 1
                                    else:
                                        ctn = False

                                if end - start > 1:
                                    for i in range(start, end):
                                        ava2[x + i][y] = False
                                        available[x + i][y] = False

                                    points.append(
                                        line(
                                            opacity=opacity,
                                            x1=x + 0.5,
                                            y1=y + 0.5,
                                            x2=x + end - start - 0.5,
                                            y2=y + 0.5,
                                            stroke_width=size,
                                            stroke=color,
                                            stroke_linecap="round",
                                        ),
                                    )

                            if available[x][y]:
                                points.append(
                                    circle(
                                        opacity=opacity,
                                        r=size / 2.0,
                                        fill=color,
                                        cx=x + 0.5,
                                        cy=y + 0.5,
                                    ),
                                )

                        if self.content_line_type == ContentLineType.radial:
                            if x > y != x + y < n_count:
                                if y == 0 or (
                                    y > 0
                                    and (not matrix[x][y - 1] or not ava2[x][y - 1])
                                ):
                                    start = 0
                                    end = 0
                                    ctn = True
                                    while ctn and y + end < n_count:
                                        if (
                                            matrix[x][y + end]
                                            and ava2[x][y + end]
                                            and end - start <= 3
                                        ):
                                            end += 1
                                        else:
                                            ctn = False

                                    if end - start > 1:
                                        for i in range(start, end):
                                            ava2[x][y + i] = False
                                            available[x][y + i] = False

                                        points.append(
                                            line(
                                                opacity=opacity,
                                                x1=x + 0.5,
                                                y1=y + 0.5,
                                                x2=x + 0.5,
                                                y2=y + end - start - 1 + 0.5,
                                                stroke_width=size,
                                                stroke=color,
                                                stroke_linecap="round",
                                            ),
                                        )

                            else:
                                if x == 0 or (
                                    x > 0
                                    and (not matrix[x - 1][y] or not ava2[x - 1][y])
                                ):
                                    start = 0
                                    end = 0
                                    ctn = True
                                    while ctn and x + end < n_count:
                                        if (
                                            matrix[x + end][y]
                                            and ava2[x + end][y]
                                            and end - start <= 3
                                        ):
                                            end += 1
                                        else:
                                            ctn = False

                                    if end - start > 1:
                                        for i in range(start, end):
                                            ava2[x + i][y] = False
                                            available[x + i][y] = False

                                        points.append(
                                            line(
                                                opacity=opacity,
                                                x1=x + 0.5,
                                                y1=y + 0.5,
                                                x2=x + end - start - 0.5,
                                                y2=y + 0.5,
                                                stroke_width=size,
                                                stroke=color,
                                                stroke_linecap="round",
                                            ),
                                        )

                            if available[x][y]:
                                points.append(
                                    circle(
                                        opacity=opacity,
                                        r=size / 2.0,
                                        fill=color,
                                        cx=x + 0.5,
                                        cy=y + 0.5,
                                    ),
                                )

                        if self.content_line_type == ContentLineType.tl_br:
                            if (
                                y == 0
                                or x == 0
                                or (
                                    y > 0
                                    and x > 0
                                    and (
                                        not matrix[x - 1][y - 1]
                                        or not ava2[x - 1][y - 1]
                                    )
                                )
                            ):
                                start = 0
                                end = 0
                                ctn = True
                                while ctn and y + end < n_count and x + end < n_count:
                                    if (
                                        matrix[x + end][y + end]
                                        and ava2[x + end][y + end]
                                    ):
                                        end += 1
                                    else:
                                        ctn = False

                                if end - start > 1:
                                    for i in range(start, end):
                                        ava2[x + i][y + i] = False
                                        available[x + i][y + i] = False

                                    points.append(
                                        line(
                                            opacity=opacity,
                                            x1=x + 0.5,
                                            y1=y + 0.5,
                                            x2=x + end - start - 1 + 0.5,
                                            y2=y + end - start - 1 + 0.5,
                                            stroke_width=size,
                                            stroke=color,
                                            stroke_linecap="round",
                                        ),
                                    )

                            if available[x][y]:
                                points.append(
                                    circle(
                                        opacity=opacity,
                                        r=size / 2.0,
                                        fill=color,
                                        cx=x + 0.5,
                                        cy=y + 0.5,
                                    ),
                                )

                        if self.content_line_type == ContentLineType.tr_bl:
                            if (
                                x == 0
                                or y == n_count - 1
                                or (
                                    x > 0
                                    and y < n_count - 1
                                    and (
                                        not matrix[x - 1][y + 1]
                                        or not ava2[x - 1][y + 1]
                                    )
                                )
                            ):
                                start = 0
                                end = 0
                                ctn = True
                                while ctn and x + end < n_count and y - end >= 0:
                                    if (
                                        matrix[x + end][y - end]
                                        and available[x + end][y - end]
                                    ):
                                        end += 1
                                    else:
                                        ctn = False

                                if end - start > 1:
                                    for i in range(start, end):
                                        ava2[x + i][y - i] = False
                                        available[x + i][y - i] = False

                                    points.append(
                                        line(
                                            opacity=opacity,
                                            x1=x + 0.5,
                                            y1=y + 0.5,
                                            x2=x + (end - start - 1) + 0.5,
                                            y2=y - (end - start - 1) + 0.5,
                                            stroke_width=size,
                                            stroke=color,
                                            stroke_linecap="round",
                                        ),
                                    )

                            if available[x][y]:
                                points.append(
                                    circle(
                                        opacity=opacity,
                                        r=size / 2.0,
                                        fill=color,
                                        cx=x + 0.5,
                                        cy=y + 0.5,
                                    ),
                                )

                        if self.content_line_type == ContentLineType.cross:
                            if (
                                x == 0
                                or y == n_count - 1
                                or (
                                    x > 0
                                    and y < n_count - 1
                                    and (
                                        not matrix[x - 1][y + 1]
                                        or not ava2[x - 1][y + 1]
                                    )
                                )
                            ):
                                start = 0
                                end = 0
                                ctn = True
                                while ctn and x + end < n_count and y - end >= 0:
                                    if (
                                        matrix[x + end][y - end]
                                        and ava2[x + end][y - end]
                                    ):
                                        end += 1
                                    else:
                                        ctn = False

                                if end - start > 1:
                                    for i in range(start, end):
                                        ava2[x + i][y - i] = False

                                    points.append(
                                        line(
                                            opacity=opacity,
                                            x1=x + 0.5,
                                            y1=y + 0.5,
                                            x2=x + (end - start - 1) + 0.5,
                                            y2=y - (end - start - 1) + 0.5,
                                            stroke_width=(size / 2.0) * random(0.3, 1),
                                            stroke=color,
                                            stroke_linecap="round",
                                        ),
                                    )

                            if (
                                y == 0
                                or x == 0
                                or (
                                    y > 0
                                    and x > 0
                                    and (
                                        not matrix[x - 1][y - 1]
                                        or not available[x - 1][y - 1]
                                    )
                                )
                            ):
                                start = 0
                                end = 0
                                ctn = True
                                while ctn and y + end < n_count and x + end < n_count:
                                    if (
                                        matrix[x + end][y + end]
                                        and available[x + end][y + end]
                                    ):
                                        end += 1
                                    else:
                                        ctn = False

                                if end - start > 1:
                                    for i in range(start, end):
                                        available[x + i][y + i] = False

                                    points.append(
                                        line(
                                            opacity=opacity,
                                            x1=x + 0.5,
                                            y1=y + 0.5,
                                            x2=x + end - start - 1 + 0.5,
                                            y2=y + end - start - 1 + 0.5,
                                            stroke_width=(size / 2.0) * random(0.3, 1),
                                            stroke=color,
                                            stroke_linecap="round",
                                        ),
                                    )

                            points.append(
                                circle(
                                    opacity=opacity,
                                    r=0.5 * random(0.33, 0.9),
                                    fill=color,
                                    cx=x + 0.5,
                                    cy=y + 0.5,
                                ),
                            )

        return points
