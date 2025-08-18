import tle2czml
import json
from pathlib import Path

base_tle_folder = Path("C:/Users/User/Code/tle2czml/tle")
tle_files = list(base_tle_folder.rglob("*.txt"))
tle_files.sort()

combined_czml = []

for i, tle_file in enumerate(tle_files):
    try:
        czml_str = tle2czml.create_czml(str(tle_file))  # This returns a JSON string
        czml_obj = json.loads(czml_str)  # Convert JSON string to Python list/dict

        if i == 0:
            combined_czml.extend(czml_obj)
        else:
            combined_czml.extend(czml_obj[1:])  # skip the first doc packet
    except Exception as e:
        print(f"Error processing {tle_file}: {e}")

output_path = "C:/Users/User/Code/tle2czml/combined_cesium.czml"

with open(output_path, 'w') as f:
    json.dump(combined_czml, f, indent=2)

print(f"Combined CZML written to {output_path}")
