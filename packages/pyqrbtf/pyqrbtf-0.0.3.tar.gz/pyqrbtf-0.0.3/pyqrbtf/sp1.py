from pyqrbtf.utils.center_module import CenterModule
from .utils.type_table import get_type_table, QRPointType


class SP1Drawer(CenterModule):
    def __init__(
        self,
        content_stroke_width=0.7,
        content_x_stroke_width=0.7,
        positioning_stroke_width=0.9,
        **kwargs,
    ):
        self.content_stroke_width = content_stroke_width
        self.content_x_stroke_width = content_x_stroke_width
        self.positioning_stroke_width = positioning_stroke_width
        super().__init__(**kwargs)

    def draw(self, matrix, colors):
        table = matrix
        type_table = get_type_table(table)

        points = []

        n_count = len(table)

        xmark_color = colors.get(QRPointType.TIMING, "#0B2D97")
        xmark_w = self.content_x_stroke_width

        content_color = colors.get(QRPointType.FORMAT, "#E02020")
        content_w = self.content_stroke_width

        important_color = colors.get(QRPointType.DATA, "#F6B506")

        line = self.line
        rect = self.rect

        available = [[True] * n_count for _ in range(n_count)]
        ava2 = [[True] * n_count for _ in range(n_count)]

        g1 = []
        g2 = []

        for y in range(n_count):
            for x in range(n_count):
                if not table[x][y]:
                    continue
                match type_table[x][y]:
                    case QRPointType.POS_OTHER:
                        continue
                    case QRPointType.POS_CENTER:
                        self.draw_center(points, colors, x, y)
                    case _:
                        if (
                            available[x][y]
                            and ava2[x][y]
                            and x < n_count - 2
                            and y < n_count - 2
                        ):
                            ctn = True
                            for i in range(3):
                                for j in range(3):
                                    try:
                                        if ava2[x + i][y + j] == False:
                                            ctn = False
                                    except IndexError:
                                        pass
                            if (
                                ctn
                                and table[x + 2][y]
                                and table[x + 1][y + 1]
                                and table[x][y + 2]
                                and table[x + 2][y + 2]
                            ):
                                g1.append(
                                    line(
                                        x1=x + xmark_w / (8**0.5),
                                        y1=y + xmark_w / (8**0.5),
                                        x2=x + 3 - xmark_w / (8**0.5),
                                        y2=y + 3 - xmark_w / (8**0.5),
                                        fill="none",
                                        stroke=xmark_color,
                                        stroke_width=xmark_w,
                                    ),
                                )
                                g1.append(
                                    line(
                                        x1=x + 3 - xmark_w / (8**0.5),
                                        y1=y + xmark_w / (8**0.5),
                                        x2=x + xmark_w / (8**0.5),
                                        y2=y + 3 - xmark_w / (8**0.5),
                                        fill="none",
                                        stroke=xmark_color,
                                        stroke_width=xmark_w,
                                    ),
                                )
                                available[x][y] = False
                                available[x + 2][y] = False
                                available[x][y + 2] = False
                                available[x + 2][y + 2] = False
                                available[x + 1][y + 1] = False
                                for i in range(3):
                                    for j in range(3):
                                        try:
                                            ava2[x + i][y + j] = False
                                        except IndexError:
                                            pass
                        if (
                            available[x][y]
                            and ava2[x][y]
                            and x < n_count - 1
                            and y < n_count - 1
                        ):
                            ctn = True
                            for i in range(2):
                                for j in range(2):
                                    try:
                                        if ava2[x + i][y + j] == False:
                                            ctn = False
                                    except IndexError:
                                        pass
                            if (
                                ctn
                                and table[x + 1][y]
                                and table[x][y + 1]
                                and table[x + 1][y + 1]
                            ):
                                g1.append(
                                    line(
                                        x1=x + xmark_w / (8**0.5),
                                        y1=y + xmark_w / (8**0.5),
                                        x2=x + 2 - xmark_w / (8**0.5),
                                        y2=y + 2 - xmark_w / (8**0.5),
                                        fill="none",
                                        stroke=xmark_color,
                                        stroke_width=xmark_w,
                                    ),
                                )
                                g1.append(
                                    line(
                                        x1=x + 2 - xmark_w / (8**0.5),
                                        y1=y + xmark_w / (8**0.5),
                                        x2=x + xmark_w / (8**0.5),
                                        y2=y + 2 - xmark_w / (8**0.5),
                                        fill="none",
                                        stroke=xmark_color,
                                        stroke_width=xmark_w,
                                    ),
                                )
                                for i in range(2):
                                    for j in range(2):
                                        try:
                                            available[x + i][y + j] = False
                                            ava2[x + i][y + j] = False
                                        except IndexError:
                                            pass
                        if available[x][y] and ava2[x][y]:
                            if y == 0 or (
                                y > 0 and (not table[x][y - 1] or not ava2[x][y - 1])
                            ):
                                start = y
                                end = y
                                ctn = True
                                while ctn and end < n_count:
                                    if table[x][end] and ava2[x][end]:
                                        end += 1
                                    else:
                                        ctn = False
                                if end - start > 2:
                                    for i in range(start, end):
                                        ava2[x][i] = False
                                        available[x][i] = False
                                    g2.append(
                                        rect(
                                            width=content_w,
                                            height=end - start - 1 - (1 - content_w),
                                            fill=content_color,
                                            x=x + (1 - content_w) / 2.0,
                                            y=y + (1 - content_w) / 2.0,
                                        ),
                                    )
                                    g2.append(
                                        rect(
                                            width=content_w,
                                            height=content_w,
                                            fill=content_color,
                                            x=x + (1 - content_w) / 2.0,
                                            y=end - 1 + (1 - content_w) / 2.0,
                                        ),
                                    )
                        if available[x][y] and ava2[x][y]:
                            if x == 0 or (
                                x > 0 and (not table[x - 1][y] or not ava2[x - 1][y])
                            ):
                                start = x
                                end = x
                                ctn = True
                                while ctn and end < n_count:
                                    if table[end][y] and ava2[end][y]:
                                        end += 1
                                    else:
                                        ctn = False
                                if end - start > 1:
                                    for i in range(start, end):
                                        ava2[i][y] = False
                                        available[i][y] = False
                                    g2.append(
                                        rect(
                                            width=end - start - (1 - content_w),
                                            height=content_w,
                                            fill=important_color,
                                            x=x + (1 - content_w) / 2.0,
                                            y=y + (1 - content_w) / 2.0,
                                        ),
                                    )
                        if available[x][y]:
                            points.append(
                                rect(
                                    width=content_w,
                                    height=content_w,
                                    fill=important_color,
                                    x=x + (1 - content_w) / 2.0,
                                    y=y + (1 - content_w) / 2.0,
                                ),
                            )
        return [*points, *g1, *g2]
