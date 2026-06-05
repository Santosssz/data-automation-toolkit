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
