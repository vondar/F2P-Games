import numpy as np
from src.engine.monte_carlo import run_monte_carlo_sim
from src.engine.validator import validate_geometric_baseline
from src.metrics.risk_metrics import calculate_risk_metrics

def test_engine_convergence():
    base_prob = 0.01
    iterations = 100000
    
    # Run simulation for geometric distribution (no pity)
    sim_data = run_monte_carlo_sim(base_prob, iterations=iterations, pity_config=None)
    
    # Validate Module 0
    validation = validate_geometric_baseline(sim_data, base_prob)
    print(f"Module 0 Validation: {validation['is_valid']}")
    print(f"Mean Error: {validation['mean']['error']:.4%}")
    
    # Calculate Risk Metrics
    metrics = calculate_risk_metrics(sim_data)
    print(f"Median Cost: {metrics['median']}")
    print(f"CTE95: {metrics['cte95']}")
    print(f"WRR: {metrics['wrr']:.2f}")
    
    return validation['is_valid']

if __name__ == "__main__":
    test_engine_convergence()
