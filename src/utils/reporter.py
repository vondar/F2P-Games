import json
import os
import numpy as np

from src.metrics.utility_decay import calculate_utility_decay
from src.utils.translator import get_human_metric, get_human_grade, GRADE_DESCRIPTIONS
from src.metrics.friction import get_grocery_equivalent

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
    snt = risk.get("safety_net_tax", 0.0)
    grade = risk.get("transparency_grade", "N/A")
    
    # 0. Plain-English Verdict
    verdict_text = ""
    if wrr > 3.0 or snt > 1.0:
        verdict_text = f"**THE VERDICT:** This banner is designed to extract surplus from 'unlucky' players. While the median player pays **${median_cost:,.2f}**, the unluckiest 5% must spend **${p95_cost:,.2f}** or more. **Recommendation: AVOID unless you have the Safe Budget ready.**"
    elif wrr > 2.0:
        verdict_text = f"**THE VERDICT:** This banner is moderately risky. Expect to pay around **${median_cost:,.2f}**, but keep **${p95_cost:,.2f}** as a buffer for bad luck."
    else:
        verdict_text = f"**THE VERDICT:** This banner is relatively fair. The price is predictable and the 'Unlucky Tax' is low."

    # Header
    summary = [
        f"# Forensic Audit: {system_name}",
        f"**Game:** {game_name}",
        f"**Date:** {os.path.basename(metadata.get('timestamp', 'N/A'))}",
        f"\n### **Forensic Grade: {get_human_grade(grade)}**",
        f"\n{verdict_text}",
        "\n---",
        "## 1. The 'Safe Budget' (Confidence Budget)",
        f"- **Median Acquisition Cost:** ${median_cost:.2f}",
        f"- **Safe Budget (95% Certainty):** ${p95_cost:.2f}",
        f"> *Acquiring this item safely requires a budget **{(p95_cost/median_cost - 1)*100:.1f}% higher** than the median player's cost.*",
        "\n## 2. The 'Unlucky Tax' (Variance)",
        f"- **The Nightmare Scenario (CTE₉₅):** ${cte95_cost:.2f}",
        f"- **Unlucky Tax (WRR):** {wrr:.2f}x",
        f"> *Unlucky players pay **{wrr:.2f} times more** than the average, indicating a heavy reliance on 'Tail Extraction'.*",
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
            big_mac_usd = data.get("big_mac_price_usd", 5.0)
            
            days_labor = p95_cost / daily_income
            big_mac_equiv = p95_cost / big_mac_usd
            grocery_math = get_grocery_equivalent(p95_cost, data)
            
            # Special emphasis for extreme labor costs
            if days_labor > 365:
                summary.append(f"- **{region}:** {days_labor/365:.1f} **YEARS** of labor ({grocery_math['months_rent']:.1f} months rent).")
            else:
                summary.append(f"- **{region}:** {days_labor:.1f} days of labor ({grocery_math['weeks_groceries']:.1f} weeks groceries).")
            
    # 5. Multi-Stage Sunk Cost Anchor
    multi_stage = config.get("multi_stage", {})
    if multi_stage.get("enabled"):
        upgrade_cost = multi_stage.get("upgrade_cost_avg_usd", 0)
        total_commitment = p95_cost + upgrade_cost
        summary.append("\n## 5. Multi-Stage Sunk Cost Anchor")
        summary.append(f"- **Base Acquisition (95%):** ${p95_cost:.2f}")
        summary.append(f"- **Estimated Upgrade Path:** ${upgrade_cost:.2f}")
        summary.append(f"- **Total Forensic Commitment:** ${total_commitment:.2f}")
        summary.append(f"> *The base skin is a **Sunk Cost Anchor**. Once acquired, the player is psychologically locked into a total commitment of **${total_commitment:.2f}** to reach full utility.*")

    summary.append("\n---")
    summary.append("**Verdict:** " + ("EXTREME RISK" if wrr > 5.0 else "HIGH RISK" if wrr > 3.0 else "MODERATE RISK"))
    
    return "\n".join(summary)

def save_report(content, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
