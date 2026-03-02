import argparse
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from src.utils.config_loader import load_loot_config
from src.engine.monte_carlo import run_monte_carlo_sim
from src.engine.validator import validate_geometric_baseline
from src.metrics.risk_metrics import calculate_risk_metrics
from src.utils.reporter import generate_forensic_summary, save_report
from src.utils.fact_sheet import generate_fact_sheet

def main():
    parser = argparse.ArgumentParser(description="F2P Monetization Analysis Runner")
    parser.add_argument("--config", type=str, required=True, help="Path to loot configuration JSON")
    parser.add_argument("--iterations", type=int, default=100000, help="Number of Monte Carlo iterations")
    parser.add_argument("--threshold", type=int, help="Number of shards/tokens required (overrides config)")
    parser.add_argument("--seed", type=int, default=42, help="PRNG seed")
    parser.add_argument("--output", type=str, default="data/results/analysis_output.json", help="Path to output results")
    parser.add_argument("--validate", action="store_true", help="Run Module 0 validation")
    parser.add_argument("--plot", action="store_true", help="Generate cost distribution plots")
    parser.add_argument("--report", action="store_true", help="Generate forensic report")
    parser.add_argument("--factsheet", action="store_true", help="Generate standardized forensic Fact Sheet")
    
    args = parser.parse_args()
    
    print(f"Loading configuration from {args.config}...")
    config = load_loot_config(args.config)
    
    base_prob = config.get("base_prob", 0.01)
    pity_config = config.get("pity_config")
    system_name = config.get("system_name", "Unknown System")
    threshold = args.threshold if args.threshold is not None else config.get("acquisition_threshold", 1)
    
    print(f"Running {args.iterations} iterations for '{system_name}' (Threshold: {threshold})...")
    sim_data = run_monte_carlo_sim(
        base_prob=base_prob,
        iterations=args.iterations,
        pity_config=pity_config,
        seed=args.seed,
        acquisition_threshold=threshold
    )
    
    results = {
        "metadata": {
            "system_name": system_name,
            "iterations": args.iterations,
            "seed": args.seed,
            "config": config,
            "timestamp": datetime.now().isoformat()
        }
    }
    
    # Module 0 Validation
    if args.validate:
        print("Running Module 0: Geometric Baseline validation...")
        validation = validate_geometric_baseline(sim_data, base_prob)
        results["validation"] = validation
        print(f"Validation Result: {'PASS' if validation['is_valid'] else 'FAIL'}")
        
    # Module 1 Risk Metrics
    print("Calculating Module 1: Risk Metrics...")
    risk_metrics = calculate_risk_metrics(sim_data)
    results["risk_metrics"] = risk_metrics
    
    # 3. CDF Plotting (Confidence Budget Framing)
    if args.plot:
        print("Generating Cost Cumulative Distribution Function (CDF) plot...")
        # Sort data to compute CDF
        x_sorted = np.sort(sim_data)
        y_cdf = np.arange(len(x_sorted)) / float(len(x_sorted))
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_sorted, y_cdf, label='Acquisition Confidence', color='tab:blue', linewidth=2)
        
        # Mark key percentiles
        median_val = risk_metrics['median']
        p95_val = risk_metrics['p95']
        
        plt.axvline(x=median_val, color='gray', linestyle='--', label=f'Median ({median_val})')
        plt.axvline(x=p95_val, color='red', linestyle='--', label=f'95% Confidence ({p95_val})')
        
        plt.xlabel('Number of Trials (Cost)')
        plt.ylabel('Cumulative Probability of Success')
        plt.title(f'Confidence Budget: {system_name}\n(95% Confidence Requires {p95_val} Pulls)')
        plt.legend()
        plt.grid(alpha=0.3)
        
        plot_path = os.path.join(os.path.dirname(args.output), "cost_cdf.png")
        plt.savefig(plot_path)
        print(f"Saved cost CDF plot to {plot_path}")
    
    # 4. Forensic Report & 5. Fact Sheet
    if args.report or args.factsheet:
        geo_config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "geo_configs.json")
        geo_data = None
        if os.path.exists(geo_config_path):
            with open(geo_config_path, "r") as f:
                geo_data = json.load(f)
        
        report_content = generate_forensic_summary(results, geo_data)
        
        if args.report:
            print("Generating Forensic Report...")
            report_path = os.path.join(os.path.dirname(args.output), f"forensic_report_{system_name.replace(' ', '_')}.md")
            save_report(report_content, report_path)
            print(f"Saved forensic report to {report_path}")
            
        if args.factsheet:
            print("Generating Standardized Fact Sheet...")
            fact_sheet_path = os.path.join(os.path.dirname(args.output), f"fact_sheet_{system_name.replace(' ', '_')}.md")
            generate_fact_sheet(results, report_content, fact_sheet_path)
            print(f"Saved Fact Sheet to {fact_sheet_path}")

    # Save results
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"\nAnalysis complete. Results saved to {args.output}")
    print(f"Median Cost: {risk_metrics['median']}")
    print(f"CTE95: {risk_metrics['cte95']}")
    print(f"Whale Revenue Ratio (WRR): {risk_metrics['wrr']:.2f}")
    print(f"Confidence Budget (95%): {risk_metrics['confidence_budget_95']}")

if __name__ == "__main__":
    main()
