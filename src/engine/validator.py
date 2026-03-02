import numpy as np
from scipy.stats import chisquare

def validate_geometric_baseline(sim_data, base_prob, tolerance=0.005):
    """
    Module 0: Geometric Baseline check.
    Validates that static probability simulations converge to analytical values.
    """
    analytical_mean = 1.0 / base_prob
    simulated_mean = np.mean(sim_data)
    
    deviation = abs(simulated_mean - analytical_mean) / analytical_mean
    is_valid = deviation < tolerance
    
    return {
        "analytical_mean": float(analytical_mean),
        "simulated_mean": float(simulated_mean),
        "deviation": float(deviation),
        "is_valid": bool(is_valid)
    }

def perform_chi_squared_test(observed_counts, expected_counts):
    """
    Performs a Chi-Squared Goodness-of-Fit test to compare observed 
    community data against simulated expectations.
    
    Returns:
        dict: p-value and verdict.
    """
    # Ensure no zeros in expected_counts to avoid division errors
    expected_counts = np.where(expected_counts == 0, 1e-9, expected_counts)
    
    # Normalize expected to match observed total
    expected_counts = expected_counts * (np.sum(observed_counts) / np.sum(expected_counts))
    
    stat, p_value = chisquare(observed_counts, f_exp=expected_counts)
    
    return {
        "statistic": float(stat),
        "p_value": float(p_value),
        "is_statistically_significant": bool(p_value < 0.05), # 95% confidence
        "verdict": "MATCH" if p_value >= 0.05 else "DISCREPANCY DETECTED"
    }
