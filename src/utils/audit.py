import hashlib
import os
import json
from datetime import datetime

def generate_file_hash(file_path):
    """
    Computes the SHA256 hash of a file.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read file in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def audit_ingested_files(ingestion_dir="data/ingestion/"):
    """
    Computes hashes for all files in the ingestion directory and returns an audit trail.
    """
    audit_trail = []
    
    if not os.path.exists(ingestion_dir):
        return audit_trail
        
    for filename in os.listdir(ingestion_dir):
        file_path = os.path.join(ingestion_dir, filename)
        if os.path.isfile(file_path):
            file_hash = generate_file_hash(file_path)
            audit_trail.append({
                "filename": filename,
                "sha256": file_hash,
                "timestamp": datetime.now().isoformat()
            })
            
    return audit_trail

def save_audit_report(audit_trail, output_path="data/results/audit_report.json"):
    """
    Saves the audit trail to a JSON file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(audit_trail, f, indent=4)
        
if __name__ == "__main__":
    # Simple CLI for auditing
    import argparse
    parser = argparse.ArgumentParser(description="F2P Screenshot Audit Utility")
    parser.add_argument("--dir", type=str, default="data/ingestion/", help="Directory to audit")
    parser.add_argument("--output", type=str, default="data/results/audit_report.json", help="Output JSON report")
    
    args = parser.parse_args()
    
    print(f"Auditing files in {args.dir}...")
    trail = audit_ingested_files(args.dir)
    save_audit_report(trail, args.output)
    
    print(f"Audit complete. Processed {len(trail)} files. Report saved to {args.output}")
