# fetcher.py

import urllib.request
import os

def load_providers(filename):
    providers = set()
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    providers.add(line)
    except FileNotFoundError:
        print(f"Provider file '{filename}' not found.")
    return providers

def fetch_tle_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                print(f"Failed to fetch TLE data. HTTP Code: {response.status}")
                return None
            data = response.read().decode('utf-8')
            return data.splitlines()
    except Exception as e:
        print(f"Error fetching TLE data: {e}")
        return None

import json

def fetch_and_save_tles(url, providers_file, output_folder, sat_ids_output):
    providers = load_providers(providers_file)
    if not providers:
        print(f"No providers found in {providers_file}")
        return False

    lines = fetch_tle_data(url)
    if not lines:
        print("No TLE data fetched.")
        return False

    os.makedirs(output_folder, exist_ok=True)

    sat_id_dict = {}

    for i in range(0, len(lines), 3):
        if i + 2 >= len(lines):
            break

        sat_name = lines[i].strip()
        line2 = lines[i + 1].strip()
        line3 = lines[i + 2].strip()

        if any(sat_name.startswith(p) for p in providers):
            sat_id = line2[2:7].strip() if len(line2) >= 7 else ""
            sat_id_dict[sat_name] = sat_id

            tle_file = os.path.join(output_folder, f"{sat_name.replace(' ', '_')}.txt")
            with open(tle_file, 'w') as f:
                f.write(f"{sat_name}\n{line2}\n{line3}\n")

    with open(sat_ids_output, 'w') as json_file:
        json.dump(sat_id_dict, json_file, indent=2)

    print(f"TLEs saved to: {output_folder}")
    print(f"Satellite IDs saved to: {sat_ids_output}")
    return True

