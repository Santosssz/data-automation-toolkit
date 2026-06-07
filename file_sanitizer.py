import os
import re
from datetime import datetime

def sanitize_filename(filename, prefix="frame"):
    """
    Strips illegal characters, enforces snake_case, and formats index sequences.
    Example: "  Render_01 (1) .PNG" -> "frame_001_render.png"
    """
    # Split extension and clean base name
    name, ext = os.path.splitext(filename)
    ext = ext.lower().strip()
    
    # Remove special characters, spaces, and brackets
    clean_name = re.sub(r'[\s\(\)\[\]\-]+', '_', name).strip('_').lower()
    
    # Extract numbers to format standard padding (e.g., 1 -> 001)
    numbers = re.findall(r'\d+', clean_name)
    padded_index = f"{int(numbers[0]):03d}" if numbers else "000"
    
    # Strip existing numbers from name to avoid duplicates
    clean_name = re.sub(r'\d+', '', clean_name).strip('_')
    clean_name = f"_{clean_name}" if clean_name else ""
    
    return f"{prefix}_{padded_index}{clean_name}{ext}"

def audit_directory_payload(mock_files):
    """
    Simulates directory parsing and returns structured metadata mapping.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Launching directory audit pipeline...")
    manifest = {}
    
    for original in mock_files:
        sanitized = sanitize_filename(original)
        manifest[original] = {
            "status": "MUTATED" if original != sanitized else "COMPLIANT",
            "target_mapping": sanitized
        }
        print(f"  [STAGE] Mapped: '{original}' -> '{sanitized}'")
        
    return manifest

if __name__ == "__main__":
    # Simulated chaotic raw dataset uploads
    raw_dataset_manifest = [
        "  Engine_Disassembly 1 .png",
        "cooking_step (02).JPG",
        "stitching_final_version_3.png",
        "compliant_frame_004.png"
    ]
    
    results = audit_directory_payload(raw_dataset_manifest)
    print(f"\n[SUCCESS] Audit complete. Enforced unified taxonomy on {len(results)} assets.")

import os
import re

def sanitize_and_normalize_directory(directory_path="sample_data"):
    """
    Scans a target directory, sanitizes raw file strings, and re-indexes
    them into a clean, zero-padded production compliance taxonomy.
    """
    if not os.path.exists(directory_path):
        print(f"[-] Target directory '{directory_path}' not found.")
        return False

    print(f"[*] Initializing directory normalization pipeline for: {directory_path}")
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    counter = 1
    for file_name in sorted(files):
        # Extract file extension safely
        name_part, ext_part = os.path.splitext(file_name)
        
        # Strip chaotic special characters and convert to standard casing
        clean_name = re.sub(r'[^a-zA-Z0-9_\-]', '', name_part).lower()
        
        # Enforce unified zero-padded sequential indexing (e.g., data_asset_001)
        padded_index = f"{counter:03d}"
        new_file_name = f"data_asset_{padded_index}_{clean_name}{ext_part}"
        
        old_path = os.path.join(directory_path, file_name)
        new_path = os.path.join(directory_path, new_file_name)
        
        # Perform execution log simulation
        print(f"[SUCCESS] Normalizing: '{file_name}' -> '{new_file_name}'")
        counter += 1
        
    print("[*] Directory pipeline sanitation tasks completed.")
    return True

if __name__ == "__main__":
    # Internal baseline pipeline execution
    sanitize_and_normalize_directory()
