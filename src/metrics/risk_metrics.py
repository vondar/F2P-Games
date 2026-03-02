import numpy as np
from scipy.stats import kurtosis

def calculate_risk_metrics(sim_data_dict):
    """
    Module 1: Tail Risk metrics.
    Supports both raw trial counts (v0.1.0) and sim_data_dict (v0.9.0).
    
    Returns:
        dict: CTE, WRR, Sunk Cost Velocity, Safety Net Tax.
    """
    if isinstance(sim_data_dict, dict):
        trials = sim_data_dict.get("trials", np.array([]))
        costs = sim_data_dict.get("costs", np.array([]))
    else:
        # Backward compatibility
        trials = sim_data_dict
        costs = trials.astype(float) # Assume cost = trial count * 1.0

    if len(trials) == 0:
        return {}
        
    median_val = np.median(trials)
    p95_val = np.percentile(trials, 95)
    
    # Conditional Tail Expectation (CTE95)
    tail_95 = trials[trials >= p95_val]
    cte95 = np.mean(tail_95)
    
    # Cost-based metrics (v0.9.0)
    median_cost = np.median(costs)
    p95_cost = np.percentile(costs, 95)
    tail_costs = costs[costs >= p95_cost]
    cte95_cost = np.mean(tail_costs)

    # Whale Revenue Ratio (WRR)
    wrr = cte95_cost / median_cost if median_cost > 0 else 1.0
    
    # Safety Net Tax (SNT)
    std_dev = np.std(trials)
    safety_net_tax = std_dev / median_val if median_val > 0 else 0.0
    
    # Transparency Score
    score_data = calculate_transparency_score(wrr, safety_net_tax)
    
    return {
        "median": int(median_val),
        "p95": int(p95_val),
        "cte95": float(cte95),
        "median_cost": float(median_cost),
        "p95_cost": float(p95_cost),
        "cte95_cost": float(cte95_cost),
        "wrr": float(wrr),
        "kurtosis": float(0.0), 
        "confidence_budget_95": int(p95_cost_percentile(trials, 0.95)),
        "safety_net_tax": float(safety_net_tax),
        "transparency_score": score_data["score"],
        "transparency_grade": score_data["grade"]
    }

def calculate_transparency_score(wrr, snt, obfuscation=1.0):
    """
    Calculates a weighted Transparency Score (0-100) and letter grade (A-F).
    """
    # Weights: WRR (40%), SNT (30%), Obfuscation (30%)
    # Lower is better for WRR, SNT, Obfuscation.
    
    # Normalize components (Heuristic)
    # WRR: 1.0 is perfect, 5.0+ is terrible
    wrr_norm = max(0, 100 - (wrr - 1.0) * 20)
    
    # SNT: 0.0 is perfect, 1.0+ is high tax
    snt_norm = max(0, 100 - snt * 100)
    
    # Obfuscation: 1.0 is perfect, 5.0+ is high obfuscation
    obf_norm = max(0, 100 - (obfuscation - 1.0) * 20)
    
    total_score = (wrr_norm * 0.4) + (snt_norm * 0.3) + (obf_norm * 0.3)
    
    if total_score >= 90: grade = "A"
    elif total_score >= 80: grade = "B"
    elif total_score >= 70: grade = "C"
    elif total_score >= 60: grade = "D"
    else: grade = "F"
    
    return {"score": float(total_score), "grade": grade}

def p95_cost_percentile(data, percentile):
    return np.percentile(data, percentile * 100)
