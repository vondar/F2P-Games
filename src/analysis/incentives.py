import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def logistic_function(x, L, x0, k, b):
    """
    Standard logistic function for modeling retention curves.
    L: Maximum value (e.g., 1.0 for 100% retention)
    x0: Midpoint (sigmoid center)
    k: Steepness
    b: Baseline retention
    """
    return L / (1 + np.exp(-k * (x - x0))) + b

def fit_retention_incentive_curve(incentive_levels, retention_outcomes):
    """
    Fits a logistic regression curve to historical player data.
    
    Args:
        incentive_levels (np.ndarray): Array of incentive values (e.g., reward value).
        retention_outcomes (np.ndarray): Boolean array of whether players stayed.
        
    Returns:
        dict: Fitted parameters, Standard Errors, and RIC Impact Score.
    """
    # Sort data for fitting
    idx = np.argsort(incentive_levels)
    x_data = incentive_levels[idx]
    y_data = retention_outcomes[idx].astype(float)
    
    # Heuristic: logistic fit using curve_fit
    try:
        # Initial guess: L=0.5, x0=mean, k=0.1, b=0.1
        p0 = [0.5, np.mean(x_data), 0.1, 0.1]
        popt, pcov = curve_fit(logistic_function, x_data, y_data, p0=p0, maxfev=10000)
        
        # Calculate standard errors from the covariance matrix diagonal
        perr = np.sqrt(np.diag(pcov))
        
        L, x0, k, b = popt
        
        # RIC Impact Score: The steepness (k) indicates how sensitive retention is to changes in incentives.
        ric_impact_score = k * 100
        
        return {
            "parameters": {
                "max_gain (L)": float(L),
                "midpoint (x0)": float(x0),
                "steepness (k)": float(k),
                "baseline (b)": float(b)
            },
            "standard_errors": {
                "L_err": float(perr[0]),
                "x0_err": float(perr[1]),
                "k_err": float(perr[2]),
                "b_err": float(perr[3])
            },
            "ric_impact_score": float(ric_impact_score),
            "correlation": float(np.corrcoef(x_data, y_data)[0, 1]),
            "is_significant": bool(perr[2] < abs(k)) # Basic significance heuristic
        }
    except Exception as e:
        return {"error": f"Fitting failed: {str(e)}"}

def simulate_player_retention_data(n_players=1000, base_retention=0.2, incentive_boost=0.5):
    """
    Generates synthetic data for testing RIC models.
    """
    # Random incentives from 0 to 100
    incentives = np.random.uniform(0, 100, n_players)
    
    # Probability of staying follows a logistic curve
    # Prob = base + boost / (1 + exp(-0.1 * (incentive - 50)))
    prob_stay = base_retention + incentive_boost / (1 + np.exp(-0.1 * (incentives - 50)))
    
    # Outcomes based on probabilities
    outcomes = np.random.random(n_players) < prob_stay
    
    return pd.DataFrame({
        "incentive_level": incentives,
        "retention": outcomes
    })
