from random import random

from .utils.center_module import CenterModule
from .utils.figure import Figure
from .utils.type_table import get_type_table, QRPointType


def rand(min_: float, max_: float) -> float:
    return random() * (max_ - min_) + min_


class CirclesDrawer(CenterModule):
    def draw(self, matrix, colors):
        size = len(matrix)
        type_table = get_type_table(matrix)
        point_list = []
        g1 = []
        g2 = []

        background_color = colors.get(QRPointType.NONE, "none")
        other_color = colors.get(QRPointType.DATA, "#000000")

        available = [[True] * size for _ in range(size)]
        ava2 = [[True] * size for _ in range(size)]

        f = Figure()
        circle = f.circle

        for y in range(size):
            for x in range(size):
                if type_table[x][y] == QRPointType.POS_OTHER:
                    continue
                elif type_table[x][y] == QRPointType.POS_CENTER:
                    self.draw_center(point_list, colors, x, y)
                else:
                    if available[x][y] and ava2[x][y] and x < size - 2 and y < size - 2:
                        ctn = True
                        for i in range(3):
                            for j in range(3):
                                if not ava2[x + i][y + j]:
                                    ctn = False
                        if (
                            ctn
                            and matrix[x + 1][y]
                            and matrix[x + 1][y + 2]
                            and matrix[x][y + 1]
                            and matrix[x + 2][y + 1]
                        ):
                            g2.append(
                                circle(
                                    cx=x + 1 + 0.5,
                                    cy=y + 1 + 0.5,
                                    r=1,
                                    fill=background_color,
                                    stroke=other_color,
                                    stroke_width=rand(0.33, 0.6),
                                )
                            )
                            if matrix[x + 1][y + 1]:
                                g1.append(
                                    circle(
                                        r=0.5 * rand(0.5, 1),
                                        fill=other_color,
                                        cx=x + 1 + 0.5,
                                        cy=y + 1 + 0.5,
                                    )
                                )
                            available[x + 1][y] = False
                            available[x][y + 1] = False
                            available[x + 2][y + 1] = False
                            available[x + 1][y + 2] = False
                            for i in range(3):
                                for j in range(3):
                                    ava2[x + i][y + j] = False

                    if x < size - 1 and y < size - 1:
                        if (
                            matrix[x][y]
                            and matrix[x + 1][y]
                            and matrix[x][y + 1]
                            and matrix[x + 1][y + 1]
                        ):
                            g1.append(
                                circle(
                                    cx=x + 1,
                                    cy=y + 1,
                                    r=0.5**0.5,
                                    fill=background_color,
                                    stroke=other_color,
                                    stroke_width=rand(0.33, 0.6),
                                )
                            )
                            for i in range(2):
                                for j in range(2):
                                    available[x + i][y + j] = False
                                    ava2[x + i][y + j] = False

                    if available[x][y] and y < size - 1:
                        if matrix[x][y] and matrix[x][y + 1]:
                            point_list.append(
                                circle(
                                    cx=x + 0.5,
                                    cy=y + 1,
                                    r=0.5 * rand(0.95, 1.05),
                                    fill=background_color,
                                    stroke=other_color,
                                    stroke_width=rand(0.36, 0.4),
                                )
                            )
                            available[x][y] = False
                            available[x][y + 1] = False

                    if available[x][y] and x < size - 1:
                        if matrix[x][y] and matrix[x + 1][y]:
                            point_list.append(
                                circle(
                                    cx=x + 1,
                                    cy=y + 0.5,
                                    r=0.5 * rand(0.95, 1.05),
                                    fill=background_color,
                                    stroke=other_color,
                                    stroke_width=rand(0.36, 0.4),
                                )
                            )
                            available[x][y] = False
                            available[x + 1][y] = False

                    if available[x][y]:
                        if matrix[x][y]:
                            point_list.append(
                                circle(
                                    cx=x + 0.5,
                                    cy=y + 0.5,
                                    r=0.5 * rand(0.5, 1),
                                    fill=other_color,
                                )
                            )

                        elif type_table[x][y] == QRPointType.DATA:
                            if rand(0, 1) > 0.85:
                                g2.append(
                                    circle(
                                        r=0.5 * rand(0.85, 1.3),
                                        cx=x + 0.5,
                                        cy=y + 0.5,
                                        fill=background_color,
                                        stroke=other_color,
                                        stroke_width=rand(0.15, 0.33),
                                    )
                                )

        point_list.extend(g1)
        point_list.extend(g2)

        return point_list
