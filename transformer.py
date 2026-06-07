import json
from datetime import datetime

def clean_and_format_data(raw_data):
    """
    Parses raw inputs into strict, command-ready structured JSON.
    """
    cleaned_records = []
    
    for item in raw_data:
        # Enforce strict uppercase tracking IDs and strip whitespace
        record_id = str(item.get("id", "")).strip().upper()
        # Clean and standardize raw text actions into clear-cut strings
        action_command = str(item.get("action", "")).strip().lower()
        
        if not record_id or not action_command:
            continue  # Skip incomplete records to ensure data integrity
            
        cleaned_records.append({
            "record_id": record_id,
            "processed_command": action_command,
            "status": "VALIDATED",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
    return cleaned_records

def save_to_json(data, output_filename="validated_output.json"):
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"[SUCCESS] Exported {len(data)} validated records to {output_filename}")
    except IOError as e:
        print(f"[ERROR] Failed to write data to file: {e}")

if __name__ == "__main__":
    # Example raw dataset simulating unorganized incoming records
    sample_raw_inputs = [
        {"id": "  idx_001 ", "action": "SAND CHAIR BACKREST "},
        {"id": "idx_002", "action": " apply varnish to wooden bench  "},
        {"id": " ", "action": "invalid record missing ID"}
    ]
    
    print("Starting data automation pipeline...")
    validated_data = clean_and_format_data(sample_raw_inputs)
    save_to_json(validated_data)

import os
import json

def run_structural_validation_pipeline(input_file="sample_data/raw_metrics_2026.json"):
    """
    Parses complex data payloads, enforces uniform schema casing,
    flags null object data corruptions, and exports structured data.
    """
    if not os.path.exists(input_file):
        print(f"[-] Data asset source '{input_file}' not found. Skipping validation pipeline.")
        return False

    print(f"[*] Extracting raw target payload from: {input_file}")
    
    with open(input_file, 'r') as file:
        try:
            raw_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"[-] Critical: Failed to parse target asset JSON. Error: {e}")
            return False

    sanitized_records = []
    print("[*] Processing schema assertions and validating parameters...")

    for index, record in enumerate(raw_data):
        # Enforce unified key schema validation (handling chaotic 'session_ID' or 'SESSION_ID')
        normalized_record = {}
        
        # Unify historical tracking key casing variations dynamically
        for key, value in record.items():
            normalized_record[key.lower()] = value
            
        session_id = normalized_record.get("session_id", f"UNKNOWN_REF_{index}")
        status = normalized_record.get("status", "UNDEFINED").upper()
        payload = normalized_record.get("payload_data", None)

        # Enforce data validation rule checks & flag data corruptions
        if payload is None:
            print(f"[FLAGGED WARNING] Token {session_id} exhibits missing object payload data.")
            status = "CORRUPTED_METADATA"
            payload = {"item_count": 0, "processTimeMs": 0}

        # Structure normalized parameters cleanly
        validated_node = {
            "session_id": session_id.upper(),
            "status": status,
            "validated_payload": {
                "item_count": int(payload.get("item_count", 0)),
                "process_time_ms": int(payload.get("processTimeMs", 0))
            }
        }
        sanitized_records.append(validated_node)

    # Output the structured engineering asset back out
    output_dir = os.path.dirname(input_file)
    output_path = os.path.join(output_dir, "clean_metrics_production.json")
    
    with open(output_path, 'w') as out_file:
        json.dump(sanitized_records, out_file, indent=2)

    print(f"[SUCCESS] Pipeline validation complete. Asset exported to: {output_path}")
    return True

if __name__ == "__main__":
    # Internal baseline execution
    run_structural_validation_pipeline()
