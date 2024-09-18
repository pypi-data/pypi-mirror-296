from xml.etree import ElementTree as ET

from .figure import Figure
from .type_table import QRPointType


class BaseDrawer:
    size = 500

    def __init__(self):
        self._figure = Figure()
        self.rect = self._figure.rect
        self.circle = self._figure.circle
        self.path = self._figure.path
        self.line = self._figure.line

    def to_bytes(
        self, matrix: list[list[bool]], colors: dict[QRPointType, str]
    ) -> bytes:
        return ET.tostring(self.svg(matrix, colors), encoding="utf-8")

    def svg(
        self, matrix: list[list[bool]], colors: dict[QRPointType, str]
    ) -> ET.Element:
        assert len(matrix) == len(matrix[0])

        n_count = len(matrix)

        view_box = [
            -n_count / 10,
            -n_count / 10,
            n_count + n_count / 10 * 2,
            n_count + n_count / 10 * 2,
        ]

        attrib = {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(self.size),
            "height": str(self.size),
            "viewBox": " ".join(map(str, view_box)),
            "class": "w-full bg-white",
        }

        et = ET.Element(
            "svg",
            attrib=attrib,
        )
        if background := colors.get(QRPointType.NONE):
            et.append(
                ET.Element(
                    "rect",
                    width="100%",
                    height="100%",
                    x=str(view_box[0]),
                    y=str(view_box[1]),
                    fill=background,
                )
            )
        for i in self.draw(matrix, colors):
            et.append(i)

        return et

    def draw(
        self, matrix: list[list[bool]], colors: dict[QRPointType, str]
    ) -> list[ET.Element]:
        raise NotImplementedError
