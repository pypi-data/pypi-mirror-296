from xml.etree import ElementTree as ET


class Figure:
    id = 0

    @staticmethod
    def _attrib(**kwargs):
        return {k.replace("_", "-"): str(v) for k, v in kwargs.items() if v is not None}

    def rect(self, **kwargs):
        el = ET.Element(
            "rect",
            id=str(self.id),
            attrib=self._attrib(**kwargs),
        )
        self.id += 1
        return el

    def circle(self, **kwargs):
        el = ET.Element(
            "circle",
            id=str(self.id),
            attrib=self._attrib(**kwargs),
        )
        self.id += 1
        return el

    def path(self, **kwargs):
        el = ET.Element(
            "path",
            id=str(self.id),
            attrib=self._attrib(**kwargs),
        )
        self.id += 1
        return el

    def line(self, **kwargs):
        el = ET.Element(
            "line",
            id=str(self.id),
            attrib=self._attrib(**kwargs),
        )
        self.id += 1
        return el
