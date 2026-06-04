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
