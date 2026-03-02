import json
import os
from datetime import datetime

def generate_fact_sheet(results_data, report_content, output_path):
    """
    Generates a standardized forensic 'Fact Sheet' in Markdown (ready for PDF export).
    """
    metadata = results_data.get("metadata", {})
    system_name = metadata.get("system_name", "Unknown System")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    fact_sheet = [
        f"# CONSUMER PROTECTION FACT SHEET: {system_name.upper()}",
        f"**Audit Timestamp:** {timestamp}",
        f"**Forensic Toolset Version:** 0.9.0",
        "\n## EXECUTIVE SUMMARY",
        "> This document provides a standardized risk assessment of a virtual loot system. "
        "It uses distributional mathematics to quantify financial exposure that is often "
        "obfuscated by virtual currencies and stochastic mechanics.",
        "\n---",
        report_content, # Include the main forensic summary
        "\n## AUDIT INTEGRITY & VERIFICATION",
        f"- **Simulation Iterations:** {metadata.get('iterations', 100000):,}",
        f"- **PRNG Seed:** {metadata.get('seed', 42)}",
        "- **Evidence Hashes:**",
    ]
    
    # Add audit trail if available
    audit_log = "data/results/audit_report.json"
    if os.path.exists(audit_log):
        with open(audit_log, "r") as f:
            trail = json.load(f)
            for entry in trail:
                fact_sheet.append(f"  - `{entry['filename']}`: {entry['sha256']}")
    else:
        fact_sheet.append("  - *No verifiable audit trail found in data/results/audit_report.json*")

    fact_sheet.append("\n---")
    fact_sheet.append("**Disclaimer:** This report is for informational purposes only. "
                     "It represents a mathematical simulation based on published rates.")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(fact_sheet))
    
    return output_path
