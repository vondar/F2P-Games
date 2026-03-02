import json
import os
import numpy as np

from src.metrics.utility_decay import calculate_utility_decay

def generate_forensic_summary(results_data, geo_data=None):
    """
    Generates a human-readable forensic summary of monetization risk.
    """
    metadata = results_data.get("metadata", {})
    risk = results_data.get("risk_metrics", {})
    config = metadata.get("config", {})
    
    system_name = metadata.get("system_name", "Unknown System")
    game_name = config.get("game", "Unknown Game")
    
    median_cost = risk.get("median_cost", 0.0)
    p95_cost = risk.get("p95_cost", 0.0)
    cte95_cost = risk.get("cte95_cost", 0.0)
    wrr = risk.get("wrr", 1.0)
    
    # Header
    summary = [
        f"# Forensic Audit: {system_name}",
        f"**Game:** {game_name}",
        f"**Date:** {os.path.basename(metadata.get('timestamp', 'N/A'))}",
        "\n---",
        "## 1. The 'Sticker Price' (Confidence Budget)",
        f"- **Median Acquisition Cost:** ${median_cost:.2f}",
        f"- **Budget for 95% Certainty:** ${p95_cost:.2f}",
        f"> *Acquiring this item with 95% confidence requires a budget **{(p95_cost/median_cost - 1)*100:.1f}% higher** than the median player's cost.*",
        "\n## 2. The 'Unlucky Player' Penalty",
        f"- **Average Cost for Unlucky 5% (CTE₉₅):** ${cte95_cost:.2f}",
        f"- **Whale Revenue Ratio (WRR):** {wrr:.2f}x",
        f"> *The unluckiest players pay **{wrr:.2f} times more** than the median, indicating significant tail-end revenue reliance.*",
    ]
    
    # 3. Utility Decay
    shelf_life = config.get("expected_meta_lifespan_days", 120)
    decay = calculate_utility_decay(median_cost, shelf_life)
    summary.append("\n## 3. Utility Shelf-Life (Meta-Relevance)")
    summary.append(f"- **Expected Meta-Relevance:** {shelf_life} days")
    summary.append(f"- **Cost Per Day of Relevance:** ${decay['daily_relevance_cost']:.2f}")
    summary.append(f"- **Effective Monthly Subscription:** ${decay['monthly_relevance_cost']:.2f}")
    summary.append(f"> *This one-time purchase is mathematically equivalent to a **${decay['monthly_relevance_cost']:.2f}/month** subscription for the duration of its meta-relevance.*")

    # 4. Labor Contextualization
    if geo_data:
        summary.append("\n## 4. Global Labor Context (Cost of Acquisition)")
        regions = geo_data.get("regions", {})
        for region, data in regions.items():
            daily_income = data.get("median_daily_income_usd", 1.0)
            days_labor = p95_cost / daily_income
            summary.append(f"- **{region}:** {days_labor:.1f} days of median labor required (95% Confidence).")
            
    summary.append("\n---")
    summary.append("**Verdict:** " + ("EXTREME RISK" if wrr > 5.0 else "HIGH RISK" if wrr > 3.0 else "MODERATE RISK"))
    
    return "\n".join(summary)

def save_report(content, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
