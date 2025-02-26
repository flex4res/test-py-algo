#!/usr/bin/env python3
import os
import json

def main():
    # 1. Read custom parameters from algoCustomData.json (if it exists).
    custom_data_path = "/data/inputs/algoCustomData.json"
    custom_params = {}
    if os.path.isfile(custom_data_path):
        with open(custom_data_path, 'r') as f:
            custom_params = json.load(f)

    # Fallback if no JSON or if 'threshold' is not provided
    threshold = custom_params.get("threshold", 10)  # default to 10
    print(f"[INFO] Using threshold = {threshold}")

    # 2. Locate input file(s) under /data/inputs.
    input_file_path = "/data/inputs/data.json"
    if not os.path.isfile(input_file_path):
        print(f"[ERROR] No input file found at {input_file_path}. Exiting.")
        return

    # 3. Process the input data (e.g., filter records by threshold).
    with open(input_file_path, 'r') as infile:
        data = json.load(infile)

    if not isinstance(data, list):
        print("[ERROR] Expected data to be a list of records. Exiting.")
        return

    filtered = [item for item in data if item.get("value", 0) >= threshold]
    print(f"[INFO] Filtered {len(filtered)} records from a total of {len(data)}.")

    # 4. Write results to /data/outputs
    output_dir = "/data/outputs"
    os.makedirs(output_dir, exist_ok=True)

    result_file_path = os.path.join(output_dir, "results.json")
    with open(result_file_path, 'w') as outfile:
        json.dump(filtered, outfile, indent=2)

    print(f"[INFO] Results written to {result_file_path}")

if __name__ == "__main__":
    main()
