import argparse
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.analysis.incentives import fit_retention_incentive_curve, simulate_player_retention_data, logistic_function

def main():
    parser = argparse.ArgumentParser(description="F2P Retention-Incentive Analysis Runner")
    parser.add_argument("--data", type=str, help="Path to historical player data CSV (optional)")
    parser.add_argument("--simulate", action="store_true", help="Simulate synthetic player data for analysis")
    parser.add_argument("--n_players", type=int, default=1000, help="Number of players for simulation")
    parser.add_argument("--output_dir", type=str, default="data/results/incentives/", help="Directory to save plots and results")
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 1. Load or Simulate Data
    if args.simulate:
        print(f"Simulating synthetic retention data for {args.n_players} players...")
        data = simulate_player_retention_data(n_players=args.n_players)
        data.to_csv(os.path.join(args.output_dir, "simulated_data.csv"), index=False)
    elif args.data:
        print(f"Loading player data from {args.data}...")
        data = pd.read_csv(args.data)
    else:
        print("Error: Must provide --data or use --simulate.")
        return
        
    # 2. Fit RIC Model
    print("Fitting Module 4: Retention Incentive Curve (RIC)...")
    incentive_levels = data["incentive_level"].values
    retention_outcomes = data["retention"].values
    
    ric_analysis = fit_retention_incentive_curve(incentive_levels, retention_outcomes)
    
    if "error" in ric_analysis:
        print(f"Fitting Error: {ric_analysis['error']}")
        return
        
    # 3. Visualization
    print("Generating Retention Incentive Curve (RIC) plot...")
    
    # Sort data for plotting
    idx = np.argsort(incentive_levels)
    x_sorted = incentive_levels[idx]
    y_sorted = retention_outcomes[idx].astype(float)
    
    # Create smooth range for curve plotting
    x_range = np.linspace(min(x_sorted), max(x_sorted), 200)
    params = ric_analysis["parameters"]
    y_fitted = logistic_function(
        x_range, 
        params["max_gain (L)"], 
        params["midpoint (x0)"], 
        params["steepness (k)"], 
        params["baseline (b)"]
    )
    
    plt.figure(figsize=(10, 6))
    
    # Scatter plot of raw data (with some jitter for binary outcomes)
    jitter = np.random.uniform(-0.02, 0.02, size=len(y_sorted))
    plt.scatter(x_sorted, y_sorted + jitter, alpha=0.1, label='Raw Player Data', color='gray')
    
    # Plot fitted curve
    plt.plot(x_range, y_fitted, color='tab:green', linewidth=3, label='Fitted RIC (Logistic)')
    
    plt.xlabel('Incentive Level (e.g., Reward Value / Unit)')
    plt.ylabel('Retention Probability')
    plt.title(f'Retention Incentive Curve (RIC)\nImpact Score: {ric_analysis["ric_impact_score"]:.2f}')
    plt.legend()
    plt.grid(alpha=0.3)
    
    plot_path = os.path.join(args.output_dir, "ric_analysis.png")
    plt.savefig(plot_path)
    print(f"Saved RIC plot to {plot_path}")
    
    # Save results
    results_path = os.path.join(args.output_dir, "ric_results.json")
    with open(results_path, 'w') as f:
        json.dump(ric_analysis, f, indent=4)
        
    print(f"\nRIC Analysis Complete. Results saved to {results_path}")
    print(f"RIC Impact Score: {ric_analysis['ric_impact_score']:.2f}")
    print(f"Midpoint (Sigmoid Center): {params['midpoint (x0)']:.2f}")
    print(f"Baseline Retention: {params['baseline (b)']:.1%}")
    print(f"Max Potential Gain: {params['max_gain (L)']:.1%}")

if __name__ == "__main__":
    main()
