# Mercator Coordinate Converter

**Mercator Coordinate Converter** is a Python package designed to simplify the conversion of geographical projection coordinates, such as latitude and longitude, into Mercator coordinates, and vice versa. This package is ideal for developers and GIS professionals who need a reliable and efficient tool for coordinate transformation.

## Installation

You can install the package using pip:

```bash
pip install MecatorConverter
```

## Usage

Here's a quick example of how to use the package:

```python
import MecatorConverter

# Convert from geographical to Mercator coordinates
latitude = 52.3676
longitude = 4.9041
mercator_x, mercator_y = MecatorConverter.coord_to_mercator(latitude, longitude)
print(f"Mercator Coordinates: X={mercator_x}, Y={mercator_y}")

# Convert from Mercator to geographical coordinates
mercator_x = 580000
mercator_y = 6800000
latitude, longitude = MecatorConverter.mercator_to_coord(mercator_x, mercator_y)
print(f"Geographical Coordinates: Latitude={latitude}, Longitude={longitude}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or need further assistance, please contact Daniil at donil858@gmail.com.
