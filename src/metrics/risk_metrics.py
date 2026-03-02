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
    
    # Whale Revenue Ratio (WRR)
    wrr = cte95 / median_val if median_val > 0 else 1.0
    
    # Safety Net Tax (SNT)
    # Comparison: Standard Deviation vs. Expected Value
    # High SNT means the system uses pity to tighten variance while potentially raising median.
    std_dev = np.std(trials)
    safety_net_tax = std_dev / median_val if median_val > 0 else 0.0
    
    return {
        "median": int(median_val),
        "p95": int(p95_val),
        "cte95": float(cte95),
        "wrr": float(wrr),
        "kurtosis": float(0.0), # Placeholder for full kurtosis
        "confidence_budget_95": int(p95_cost_percentile(trials, 0.95)),
        "safety_net_tax": float(safety_net_tax)
    }

def p95_cost_percentile(data, percentile):
    return np.percentile(data, percentile * 100)
