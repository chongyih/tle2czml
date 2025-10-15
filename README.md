# Satellite TLE to CZML Converter

Converts Two-Line Element (TLE) data for satellites into CZML format for visualization.

## Files

- **Provider.txt** - List of satellites to track
- **Converter.py** - Fetches TLEs from [Celestrak](https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle) and generates CZML

## Configuration

Edit satellite colors in `converter.py`:
```python
SATELLITE_COLOR_MAP = {
    "DS-EO": [255, 0, 255, 255],      # Magenta
    "DS-SAR": [255, 200, 0, 255],     # Orange
    "TELEOS-2": [0, 255, 255, 255],   # Cyan
    "UMBRA": [255, 255, 255, 255]     # White
}
```

## Usage

1. Generate TLE and CZML files:
```bash
python3 converter.py
```

2. Copy output to project:
```bash
cp czml/$(date +%Y-%m-%d)/combined.czml ~/git/commercial-tasking/public
```

## Output

Generated files are saved to `czml/YYYY-MM-DD/combined.czml`