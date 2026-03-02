import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
from src.analysis.sensitivity import delta_risk_sweep, soft_pity_impact_analysis
from src.utils.config_loader import load_loot_config

def main():
    parser = argparse.ArgumentParser(description="F2P Sensitivity Analysis & Visualization")
    parser.add_argument("--config", type=str, required=True, help="Path to loot configuration JSON")
    parser.add_argument("--iterations", type=int, default=100000, help="Number of iterations")
    parser.add_argument("--output_dir", type=str, default="data/results/sensitivity/", help="Directory to save plots")
    
    args = parser.parse_args()
    
    config = load_loot_config(args.config)
    base_prob = config.get("base_prob", 0.006)
    pity_config = config.get("pity_config")
    system_name = config.get("system_name", "System")
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 1. Soft Pity Impact Analysis
    if pity_config and pity_config.get("type") == "linear":
        print("Running Soft Pity Impact Analysis...")
        start_orig = pity_config.get("start", 74)
        end_orig = pity_config.get("end", 90)
        
        # Test pity starts from -10 to +5 around the original
        pity_range = range(max(1, start_orig - 10), min(end_orig, start_orig + 6))
        
        impact_results = soft_pity_impact_analysis(
            base_prob=base_prob,
            pity_start_range=list(pity_range),
            pity_end=end_orig,
            iterations=args.iterations
        )
        
        # Plotting
        starts = [r["pity_start"] for r in impact_results]
        cte95s = [r["cte95"] for r in impact_results]
        wrrs = [r["wrr"] for r in impact_results]
        
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        color = 'tab:red'
        ax1.set_xlabel('Pity Start Trial')
        ax1.set_ylabel('CTE95 (Unlucky 5% Cost)', color=color)
        ax1.plot(starts, cte95s, marker='o', color=color, label='CTE95')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.axvline(x=start_orig, color='gray', linestyle='--', label=f'Original Start ({start_orig})')
        
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Whale Revenue Ratio (WRR)', color=color)
        ax2.plot(starts, wrrs, marker='s', color=color, label='WRR')
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title(f'Sensitivity Analysis: Pity Trigger Impact on Tail Risk\n({system_name})')
        fig.tight_layout()
        plt.savefig(os.path.join(args.output_dir, "pity_sensitivity.png"))
        print(f"Saved pity sensitivity plot to {args.output_dir}")

    # 2. Delta-Risk Sweep
    print("Running Delta-Risk Sweep...")
    delta_results = delta_risk_sweep(
        base_prob=base_prob,
        pity_config=pity_config,
        delta=0.0005, # 0.05% shift
        iterations=args.iterations
    )
    
    print(f"\nDelta-Risk Analysis (0.05% reduction in base prob):")
    print(f"Delta CTE95: {delta_results['delta_cte95']:.2f}")
    print(f"Delta WRR: {delta_results['delta_wrr']:.4%}")
    
    # Save delta-risk results
    with open(os.path.join(args.output_dir, "delta_risk.json"), "w") as f:
        import json
        json.dump(delta_results, f, indent=4)

if __name__ == "__main__":
    main()
