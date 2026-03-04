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
    
    risk = results_data.get("risk_metrics", {})
    grade = risk.get("transparency_grade", "N/A")
    score = risk.get("transparency_score", 0.0)
    snt = risk.get("safety_net_tax", 0.0)

    fact_sheet = [
        f"# CONSUMER PROTECTION FACT SHEET: {system_name.upper()}",
        f"**Audit Timestamp:** {timestamp}",
        f"**Forensic Toolset Version:** 1.0.0",
        "\n## EXECUTIVE SUMMARY",
        "> This document provides a standardized risk assessment of a virtual loot system. "
        "It uses distributional mathematics to quantify financial exposure that is often "
        "obfuscated by virtual currencies and stochastic mechanics.",
        f"\n### **FORENSIC GRADE: {grade}** ({score:.1f}/100)",
        f"- **Safety Net Tax (SNT):** {snt:.2f}",
        "> *The SNT measures how much of the price is 'taxed' into the pity system vs. raw luck.*",
    ]

    # Add sensitivity sweep summary for low-transparency systems
    if "sensitivity_sweep" in results_data:
        fact_sheet.append("\n### **TRANSPARENCY TRAP: SENSITIVITY SWEEP**")
        fact_sheet.append("> This system has an undisclosed or ultra-low base probability. We analyzed the 'Confidence Budget' required if the real rate is lower than published.")
        sweeps = results_data["sensitivity_sweep"]
        for prob, cost in sweeps.items():
            fact_sheet.append(f"- **If real rate is {float(prob)*100:.2f}%:** 95% Confidence requires **${cost:,.2f}**.")

    fact_sheet.append("\n---")
    fact_sheet.append(report_content) # Include the main forensic summary
    
    fact_sheet.extend([
        "\n## AUDIT INTEGRITY & VERIFICATION",
        f"- **Simulation Iterations:** {metadata.get('iterations', 100000):,}",
        f"- **PRNG Seed:** {metadata.get('seed', 42)}",
        "- **Evidence Hashes:**",
    ])
    
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
