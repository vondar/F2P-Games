import numpy as np
from src.engine.curves import get_pity_prob, get_trial_cost

def run_monte_carlo_sim(base_prob, iterations=100000, pity_config=None, seed=42, acquisition_threshold=1, base_cost_usd=1.0, secondary_logic=None, mode="geometric"):
    """
    Module 1: Vectorized Monte Carlo simulation core.
    Supports:
    - Multi-Stage Acquisition
    - Step-Up (Variable Cost/Prob)
    - Conditional Guarantees (e.g., Genshin 50/50)
    - Mode: "geometric" (standard loot box) or "exhaustive" (Lucky Draw/Hypergeometric)
    """
    np.random.seed(seed)
    
    trials_until_acquisition = np.zeros(iterations, dtype=int)
    costs_until_acquisition = np.zeros(iterations, dtype=float)
    success_counts = np.zeros(iterations, dtype=int)
    
    guarantee_state = np.zeros(iterations, dtype=int)
    active_mask = np.ones(iterations, dtype=bool)
    current_trial = 1
    pity_counters = np.zeros(iterations, dtype=int)
    
    # Handle initial discount (e.g., first pull is 10 UC vs 60 UC)
    initial_discount = secondary_logic.get("initial_discount_usd") if secondary_logic else None

    # For exhaustive mode, we need to track pool state per iteration
    if mode == "exhaustive":
        # items_in_pool = secondary_logic.get("items_in_pool", 10)
        # target_item_index = 0
        # Instead of full pool tracking, we track target probability which increases as items are removed
        # For CODM Lucky Draw, the target is usually the last item.
        # We model this by increasing p_success as current_trial increases, 
        # based on a list of probabilities for each pull.
        pass

    max_trials = 8000
    if pity_config and "end" in pity_config:
        max_trials = max(max_trials, (pity_config["end"] + 1) * acquisition_threshold * 3)
    if mode == "exhaustive":
        max_trials = secondary_logic.get("max_pulls", 10) + 1

    while np.any(active_mask) and current_trial < max_trials:
        num_active = np.sum(active_mask)
        active_indices = np.where(active_mask)[0]
        
        pity_counters[active_indices] += 1
        
        # 1. Resolve Probability
        if mode == "exhaustive":
            # In exhaustive mode, probabilities are fixed per pull index
            probs_list = secondary_logic.get("exhaustive_probs", [])
            p_success = probs_list[current_trial-1] if (current_trial-1) < len(probs_list) else 1.0
        else:
            p_success = np.array([get_pity_prob(pity_counters[idx], base_prob, pity_config) for idx in active_indices])
        
        # 2. Resolve Cost
        if current_trial == 1 and initial_discount is not None:
            trial_cost = initial_discount
        elif mode == "exhaustive":
            costs_list = secondary_logic.get("exhaustive_costs_usd", [])
            trial_cost = costs_list[current_trial-1] if (current_trial-1) < len(costs_list) else base_cost_usd
        else:
            trial_cost = np.array([get_trial_cost(pity_counters[idx], base_cost_usd, pity_config) for idx in active_indices])
        
        outcomes = np.random.random(num_active) < p_success
        
        costs_until_acquisition[active_indices] += trial_cost
        successful_active_indices = active_indices[outcomes]
        
        if len(successful_active_indices) > 0:
            if mode == "geometric" and secondary_logic:
                logic_type = secondary_logic.get("type")
                if logic_type == "binary_flip_with_guarantee":
                    # ... existing 50/50 logic ...
                    target_chance = secondary_logic.get("target_chance", 0.5)
                    on_guarantee = guarantee_state[successful_active_indices] == 1
                    not_on_guarantee_indices = successful_active_indices[~on_guarantee]
                    flip_results = np.random.random(len(not_on_guarantee_indices)) < target_chance
                    target_won_mask = np.zeros(len(successful_active_indices), dtype=bool)
                    target_won_mask[on_guarantee] = True
                    target_won_mask[~on_guarantee] = flip_results
                    target_wins = successful_active_indices[target_won_mask]
                    target_losses = successful_active_indices[~target_won_mask]
                    guarantee_state[target_wins] = 0
                    guarantee_state[target_losses] = 1
                    success_counts[target_wins] += 1
                elif logic_type == "epitomized_path":
                    # ... existing epitomized logic ...
                    target_chance = secondary_logic.get("target_chance", 0.375)
                    max_fails = secondary_logic.get("max_fails", 2)
                    on_guarantee = guarantee_state[successful_active_indices] >= max_fails
                    not_on_guarantee_indices = successful_active_indices[~on_guarantee]
                    flip_results = np.random.random(len(not_on_guarantee_indices)) < target_chance
                    target_won_mask = np.zeros(len(successful_active_indices), dtype=bool)
                    target_won_mask[on_guarantee] = True
                    target_won_mask[~on_guarantee] = flip_results
                    target_wins = successful_active_indices[target_won_mask]
                    target_losses = successful_active_indices[~target_won_mask]
                    guarantee_state[target_wins] = 0
                    guarantee_state[target_losses] += 1
                    success_counts[target_wins] += 1
                else:
                    success_counts[successful_active_indices] += 1
            else:
                # exhaustive or standard geometric success
                success_counts[successful_active_indices] += 1
            
            pity_counters[successful_active_indices] = 0
            finished_mask = success_counts[successful_active_indices] >= acquisition_threshold
            finished_indices = successful_active_indices[finished_mask]
            
            if len(finished_indices) > 0:
                trials_until_acquisition[finished_indices] = current_trial
                active_mask[finished_indices] = False
        
        current_trial += 1
        
    return {
        "trials": trials_until_acquisition,
        "costs": costs_until_acquisition
    }
