# PyQrbtf

pyqrbtf is a Python library for generating beautiful and customizable QR codes in SVG format. It is a Python port of the original [qrbtf JavaScript library](https://github.com/latentcat/qrbtf).

## Features

- Generate aesthetically pleasing QR codes
- Multiple style options for QR code rendering
- SVG output for high-quality, scalable QR codes
- Customizable colors, shapes, and patterns
- Easy-to-use Python API

## Installation

You can install pyqrbtf using pip:

```bash
pip install pyqrbtf
```

## Usage

Here's a quick example of how to use pyqrbtf:

```python
from qrcode import QRCode
from pyqrbtf import PositioningPointType, SP1Drawer

qr = QRCode(
    version=1,
    error_correction=1,
    box_size=10,
    border=0,
)

qr.add_data("test")
qr.make()

a = SP1Drawer(positioning_point_type=PositioningPointType.circle)
text = a.to_bytes(qr.get_matrix(), {})
with open("example.svg", "wb") as f:
    f.write(text)
```

## Documentation

Will be created after 100 stars in this repo

## Examples

You can find example outputs in the `examples/` directory:

| circles_circle | circles_circle_rounded | sp1_rounded |
| --- | --- | --- |
| ![circles_circle](/examples/circles_circle.svg) | ![circles_circle_rounded](/examples/dots_planet_circle.svg) | ![sp1_rounded](/examples/sp1_rounded.svg) |


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Original [qrbtf JavaScript library](https://github.com/latentcat/qrbtf) by latentcat
- [Python QR Code](https://github.com/lincolnloop/python-qrcode) library

## Contact

If you have any questions or feedback, please open an issue here.