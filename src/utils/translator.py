"""
Translator utility to bridge the gap between technical forensic metrics
and "Human" consequences.
"""

METRIC_TRANSLATIONS = {
    "95% Confidence Budget": {
        "human_name": "The 'Safe' Budget",
        "tooltip": "If you want to be 95% sure you actually get the item, this is what you MUST have in your wallet. Anything less is a high-risk gamble."
    },
    "Whale Revenue Ratio (WRR)": {
        "human_name": "The Unlucky Tax",
        "tooltip": "How much more do the unluckiest players pay compared to the average? (e.g., 5x means you're paying 5 times the price just for being unlucky)."
    },
    "CTE95": {
        "human_name": "The Nightmare Scenario",
        "tooltip": "The average amount spent by the unluckiest 5% of players. This is your reality if you have 'Bad Luck'."
    },
    "Safety Net Tax (SNT)": {
        "human_name": "The Hidden Pity Cost",
        "tooltip": "How much of the price is 'taxed' into the guarantee system rather than pure luck. A high tax means the game forces you to pay for the 'Safety Net'."
    },
    "Loss Aversion Index (LAI)": {
        "human_name": "The Sunk Cost Trap",
        "tooltip": "Quantifies the psychological pressure to keep spending once you've started. Your brain overvalues the next pull because of what you've already lost."
    }
}

GRADE_DESCRIPTIONS = {
    "A": "Fair & Transparent",
    "B": "Predictable but Expensive",
    "C": "Moderate Risk (Variance Trap)",
    "D": "High Risk (Predatory Architecture)",
    "F": "Mathematically Dangerous (Avoid)"
}

def get_human_metric(technical_name):
    """Returns the human-friendly name and tooltip for a technical metric."""
    return METRIC_TRANSLATIONS.get(technical_name, {
        "human_name": technical_name,
        "tooltip": ""
    })

def get_human_grade(grade):
    """Returns a human-friendly description for a forensic grade."""
    return f"{grade} ({GRADE_DESCRIPTIONS.get(grade, 'Unknown Risk')})"

def get_sunk_cost_warning(shards, total, cost_per_pull):
    """Generates a visceral warning based on shard progress."""
    if total <= 0: return "No acquisition threshold defined."
    ratio = shards / total
    
    if ratio >= 0.8:
        # Calculate perceived value (Heuristic: 1/(1-ratio))
        perceived_val = cost_per_pull / (1.0 - ratio) if ratio < 1.0 else 1000.0
        return f"🚨 DANGER: You are {int(ratio*100)}% done. Your brain thinks the next pull is worth **${perceived_val:.2f}**, even though it only costs **${cost_per_pull:.2f}**. You are now being manipulated by the Sunk Cost Trap."
    elif ratio >= 0.5:
        return f"⚠️ WARNING: You are halfway there. The psychological pressure to 'not waste' your progress is starting to outweigh financial logic."
    return "You are still in the 'Low Commitment' zone. It is safe to stop now without major psychological loss."
