import numpy as np
from src.engine.monte_carlo import run_monte_carlo_sim
from src.metrics.risk_metrics import calculate_risk_metrics

def delta_risk_sweep(base_prob, pity_config, delta=0.0005, iterations=100000):
    """
    Module 4: Delta-Risk sweeps.
    Evaluates how small shifts in probability affect tail risk.
    
    Delta TR = TailRisk(p) - TailRisk(p - delta)
    """
    # Base case
    sim_base = run_monte_carlo_sim(base_prob, iterations=iterations, pity_config=pity_config)
    risk_base = calculate_risk_metrics(sim_base)
    
    # Delta case (reduced probability)
    prob_delta = base_prob - delta
    sim_delta = run_monte_carlo_sim(prob_delta, iterations=iterations, pity_config=pity_config)
    risk_delta = calculate_risk_metrics(sim_delta)
    
    # Calculate Delta-Risk
    delta_cte95 = risk_delta["cte95"] - risk_base["cte95"]
    delta_wrr = risk_delta["wrr"] - risk_base["wrr"]
    
    return {
        "base_prob": float(base_prob),
        "delta_prob": float(prob_delta),
        "delta_cte95": float(delta_cte95),
        "delta_wrr": float(delta_wrr),
        "risk_base": risk_base,
        "risk_delta": risk_delta
    }

def soft_pity_impact_analysis(base_prob, pity_start_range, pity_end, iterations=100000):
    """
    Evaluates the financial impact of moving soft pity triggers.
    
    Args:
        base_prob (float): Base probability.
        pity_start_range (list of int): Range of trials where soft pity could start.
        pity_end (int): Hard pity trial.
        
    Returns:
        list of dict: Risk metrics for each pity start trigger.
    """
    results = []
    for start in pity_start_range:
        pity_config = {"start": start, "end": pity_end}
        sim = run_monte_carlo_sim(base_prob, iterations=iterations, pity_config=pity_config)
        risk = calculate_risk_metrics(sim)
        risk["pity_start"] = start
        results.append(risk)
        
    return results
