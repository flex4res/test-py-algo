#!/usr/bin/env python3
"""
CtD Algorithm Template
----------------------
This template demonstrates how to structure a Python algorithm for
a Compute-to-Data environment (e.g., Pontus-X). It separates the
“static” parts required by CtD from the “algorithm logic” parts that
users can customize.

Key points:
- Reads optional custom parameters from /data/inputs/algoCustomData.json.
- Searches for an input data file in /data/inputs (ignoring algoCustomData.json).
- Parses the data (assumed to be JSON).
- Applies a user-defined transformation (the “algorithm logic”).
- Writes results to /data/outputs/results.json.

Directory Layout in CtD:
- /data/inputs:  Contains input data and algoCustomData.json (if any).
- /data/outputs: Should contain the final results after processing.
"""

import os
import glob
import json


def read_custom_params():
    """
    Reads optional custom parameters from /data/inputs/algoCustomData.json.
    Returns a dictionary of parameters. If not found, returns {}.
    """
    custom_data_path = "/data/inputs/algoCustomData.json"
    if os.path.isfile(custom_data_path):
        with open(custom_data_path, 'r') as f:
            return json.load(f)
    return {}


def find_input_file():
    """
    Searches /data/inputs for the first file that is not algoCustomData.json.
    Returns the path to that file, or None if none found.
    """
    all_files = glob.glob("/data/inputs/**/*", recursive=True)
    candidate_files = [
        f for f in all_files
        if os.path.isfile(f) and os.path.basename(f) != "algoCustomData.json"
    ]
    if not candidate_files:
        return None
    return candidate_files[0]


def parse_json_file(file_path):
    """
    Opens the file at file_path and parses it as JSON.
    Returns the parsed object (expected to be a list/dict).
    Raises an exception if parsing fails.
    """
    with open(file_path, 'r') as infile:
        return json.load(infile)


def user_algorithm(data, threshold):
    """
    USER ALGORITHM LOGIC:
    ---------------------
    Replace or extend this function with the core logic of your algorithm.
    Below is a simple example that filters records in a list
    where 'value' >= threshold.

    'data' is the parsed JSON object (often a list of records).
    'threshold' is a custom parameter.

    Returns the processed/filtered data.
    """
    # Example: if data is a list of dicts, each with a "value" key.
    if not isinstance(data, list):
        raise ValueError("Expected input data to be a list of records.")

    filtered = [item for item in data if item.get("value", 0) >= threshold]
    return filtered


def write_results(data):
    """
    Writes the final processed data to /data/outputs/results.json.
    """
    output_dir = "/data/outputs"
    os.makedirs(output_dir, exist_ok=True)
    result_file_path = os.path.join(output_dir, "results.json")

    with open(result_file_path, 'w') as outfile:
        json.dump(data, outfile, indent=2)

    print(f"[INFO] Results written to {result_file_path}")


def main():
    """
    MAIN ENTRY POINT:
    1. Read custom parameters (threshold).
    2. Locate input file in /data/inputs.
    3. Parse the JSON data.
    4. Run user-defined algorithm logic.
    5. Write results to /data/outputs.
    """

    # 1. Read custom parameters
    custom_params = read_custom_params()
    threshold = custom_params.get("threshold", 10)
    print(f"[INFO] Using threshold = {threshold}")

    # 2. Locate input file
    input_file_path = find_input_file()
    if not input_file_path:
        print("[ERROR] No input file found in /data/inputs. Exiting.")
        return
    print(f"[INFO] Found file at {input_file_path}. Attempting to parse as JSON...")

    # 3. Parse the JSON data
    try:
        data = parse_json_file(input_file_path)
    except Exception as e:
        print(f"[ERROR] Could not parse {input_file_path} as JSON: {e}")
        return

    # 4. Apply user algorithm logic
    try:
        processed_data = user_algorithm(data, threshold)
        print(f"[INFO] Processed {len(processed_data)} records out of {len(data)}.")
    except Exception as e:
        print(f"[ERROR] Algorithm logic failed: {e}")
        return

    # 5. Write results to /data/outputs
    write_results(processed_data)


if __name__ == "__main__":
    main()
