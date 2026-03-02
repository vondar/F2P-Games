import numpy as np

def linear_pity_curve(current_trial, pity_start, pity_end, base_prob, target_prob=1.0):
    """
    Calculates the probability of success for a given trial based on a linear soft pity curve.
    
    Args:
        current_trial (int or np.ndarray): The current trial number (1-indexed).
        pity_start (int): The trial where soft pity begins.
        pity_end (int): The trial where success is guaranteed (hard pity).
        base_prob (float): The base probability before soft pity.
        target_prob (float): The maximum probability reached at pity_end.
        
    Returns:
        float or np.ndarray: The probability of success.
    """
    if isinstance(current_trial, (int, float)):
        if current_trial < pity_start:
            return base_prob
        if current_trial >= pity_end:
            return target_prob
        
        # Linear interpolation
        slope = (target_prob - base_prob) / (pity_end - pity_start)
        return base_prob + slope * (current_trial - pity_start)
    else:
        # NumPy vectorized implementation
        probs = np.full_like(current_trial, base_prob, dtype=float)
        
        mask_pity = (current_trial >= pity_start) & (current_trial < pity_end)
        slope = (target_prob - base_prob) / (pity_end - pity_start)
        probs[mask_pity] = base_prob + slope * (current_trial[mask_pity] - pity_start)
        
        probs[current_trial >= pity_end] = target_prob
        return probs

def exponential_pity_curve(current_trial, pity_start, base_prob, factor=1.1):
    """
    An alternative soft pity curve where probability grows exponentially.
    """
    if isinstance(current_trial, (int, float)):
        if current_trial < pity_start:
            return base_prob
        return min(1.0, base_prob * (factor ** (current_trial - pity_start + 1)))
    else:
        probs = np.full_like(current_trial, base_prob, dtype=float)
        mask = current_trial >= pity_start
        probs[mask] = np.minimum(1.0, base_prob * (factor ** (current_trial[mask] - pity_start + 1)))
        return probs

def get_pity_prob(current_trial, base_prob, config):
    """
    Generic probability resolver based on configuration.
    Supports 'step-up' sequences with trial-specific overrides.
    """
    if not config:
        return base_prob
    
    # Check for Step-Up overrides (trial-specific p)
    if "step_up" in config:
        # Check if current trial has a specific probability
        # step_up is expected to be a dict: {trial_num: prob}
        step_overrides = config.get("step_up", {})
        if str(current_trial) in step_overrides:
            return step_overrides[str(current_trial)]
        
    curve_type = config.get("type", "linear")
    
    if curve_type == "linear":
        return linear_pity_curve(
            current_trial, 
            config.get("start", 70), 
            config.get("end", 90), 
            base_prob,
            config.get("target_prob", 1.0)
        )
    elif curve_type == "exponential":
        return exponential_pity_curve(
            current_trial,
            config.get("start", 70),
            base_prob,
            config.get("factor", 1.1)
        )
    else:
        # Default to base prob if type unknown
        return base_prob

def get_trial_cost(trial, base_cost, config=None):
    """
    Returns the cost for a specific trial number.
    Supports 'step-up' sequences with trial-specific costs.
    """
    if config and "step_up_costs" in config:
        costs = config.get("step_up_costs", {})
        if str(trial) in costs:
            return costs[str(trial)]
            
    return base_cost
