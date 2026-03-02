import numpy as np
from src.engine.monte_carlo import run_monte_carlo_sim

def simulate_seasonal_load(banner_configs, iterations=100000, seed=42):
    """
    Simulates a 'Season' where a player interacts with multiple stochastic systems.
    
    Args:
        banner_configs (list): List of loot config dictionaries for the season.
        iterations (int): Number of independent seasons to simulate.
        
    Returns:
        dict: Seasonal tail coincidence and cumulative cost distribution.
    """
    seasonal_costs = np.zeros(iterations)
    individual_percentiles = []
    
    for i, config in enumerate(banner_configs):
        res = run_monte_carlo_sim(
            base_prob=config.get("base_prob", 0.01),
            iterations=iterations,
            pity_config=config.get("pity_config"),
            seed=seed + i,
            acquisition_threshold=config.get("acquisition_threshold", 1),
            base_cost_usd=config.get("cost_per_pull_usd", 1.0)
        )
        
        costs = res["costs"]
        seasonal_costs += costs
        
        # Calculate P80 threshold for this specific banner
        p80 = np.percentile(costs, 80)
        is_unlucky = costs >= p80
        individual_percentiles.append(is_unlucky)
        
    # Coincidence: How many players were 'unlucky' (P80+) in ALL banners?
    coincidence_mask = np.all(individual_percentiles, axis=0)
    coincidence_rate = np.mean(coincidence_mask)
    
    return {
        "cumulative_costs": seasonal_costs,
        "coincidence_rate": float(coincidence_rate),
        "median_seasonal_cost": float(np.median(seasonal_costs)),
        "p95_seasonal_cost": float(np.percentile(seasonal_costs, 95)),
        "black_swan_risk": float(coincidence_rate * 100) # Percentage
    }
