import json
import os
from pathlib import Path
from datetime import datetime

from tle2czml import create_czml
from tle2czml.fetcher import fetch_and_save_tles

# Config
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
PROVIDERS_FILE = "providers.txt"
BASE_TLE_DIR = Path("tle")
BASE_CZML_DIR = Path("czml")
DATE_STR = datetime.now().strftime("%Y-%m-%d")
TLE_OUTPUT_FOLDER = BASE_TLE_DIR / DATE_STR
SAT_IDS_OUTPUT = TLE_OUTPUT_FOLDER / "satellite_ids.json"
COMBINED_CZML_OUTPUT = BASE_CZML_DIR / DATE_STR / "combined.czml"

def convert_and_combine_to_czml():
    os.makedirs(COMBINED_CZML_OUTPUT.parent, exist_ok=True)

    tle_files = list(TLE_OUTPUT_FOLDER.glob("*.txt"))
    tle_files.sort()

    combined_czml = []

    for i, tle_file in enumerate(tle_files):
        try:
            czml_str = create_czml(str(tle_file), COMBINED_CZML_OUTPUT)
            czml_obj = json.loads(czml_str)

            if i == 0:
                combined_czml.extend(czml_obj)
            else:
                combined_czml.extend(czml_obj[1:])  # skip the document packet
        except Exception as e:
            print(f"Error processing {tle_file.name}: {e}")

    with open(COMBINED_CZML_OUTPUT, 'w') as f:
        json.dump(combined_czml, f, indent=2)

    print(f"✅ Combined CZML written to: {COMBINED_CZML_OUTPUT}")

def main():
    success = fetch_and_save_tles(
        TLE_URL, 
        PROVIDERS_FILE, 
        str(TLE_OUTPUT_FOLDER), 
        str(SAT_IDS_OUTPUT)
    )
    if success:
        convert_and_combine_to_czml()

if __name__ == "__main__":
    main()