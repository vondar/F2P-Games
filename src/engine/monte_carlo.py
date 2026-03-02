import numpy as np
from src.engine.curves import get_pity_prob

def run_monte_carlo_sim(base_prob, iterations=100000, pity_config=None, seed=42, acquisition_threshold=1, base_cost_usd=1.0):
    """
    Module 1: Vectorized Monte Carlo simulation core.
    Supports Multi-Stage Acquisition and Step-Up (Variable Cost/Prob).
    
    Returns:
        dict: {
            "trials": np.ndarray,
            "costs": np.ndarray # Total USD cost per iteration
        }
    """
    np.random.seed(seed)
    
    trials_until_acquisition = np.zeros(iterations, dtype=int)
    costs_until_acquisition = np.zeros(iterations, dtype=float)
    success_counts = np.zeros(iterations, dtype=int)
    
    active_mask = np.ones(iterations, dtype=bool)
    current_trial = 1
    
    max_trials = 2000 
    if pity_config and "end" in pity_config:
        max_trials = max(max_trials, (pity_config["end"] + 1) * acquisition_threshold)

    while np.any(active_mask) and current_trial < max_trials:
        num_active = np.sum(active_mask)
        
        p_success = get_pity_prob(current_trial, base_prob, pity_config)
        trial_cost = get_trial_cost(current_trial, base_cost_usd, pity_config)
        
        outcomes = np.random.random(num_active) < p_success
        
        active_indices = np.where(active_mask)[0]
        
        # All active simulations pay for this trial
        costs_until_acquisition[active_indices] += trial_cost
        
        successful_indices = active_indices[outcomes]
        success_counts[successful_indices] += 1
        
        finished_indices = successful_indices[success_counts[successful_indices] >= acquisition_threshold]
        
        if len(finished_indices) > 0:
            trials_until_acquisition[finished_indices] = current_trial
            active_mask[finished_indices] = False
        
        current_trial += 1
        
    return {
        "trials": trials_until_acquisition,
        "costs": costs_until_acquisition
    }
