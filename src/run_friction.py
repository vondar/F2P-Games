import argparse
import os
import json
from src.utils.config_loader import load_loot_config
from src.metrics.friction import calculate_incentive_gap, calculate_conversion_loss_factor

def main():
    parser = argparse.ArgumentParser(description="F2P Friction & Obfuscation Analysis Runner")
    parser.add_argument("--config", type=str, required=True, help="Path to friction configuration JSON")
    parser.add_argument("--output", type=str, default="data/results/friction_analysis.json", help="Path to output results")
    
    args = parser.parse_args()
    
    print(f"Loading friction config from {args.config}...")
    config = load_loot_config(args.config)
    
    system_name = config.get("system_name", "Unknown System")
    required_cost = config.get("required_acquisition_cost", 2500)
    available_packs = config.get("available_packs", [])
    exchange_rates = config.get("exchange_rates", {})
    
    print(f"Analyzing friction for '{system_name}'...")
    
    # 1. Incentive Gap (IG)
    # Measures forced surplus spending.
    gap_analysis = calculate_incentive_gap(required_cost, available_packs)
    
    # 2. Conversion Loss Factor
    # Measures complexity of exchange rates.
    conversion_analysis = calculate_conversion_loss_factor(exchange_rates)
    
    results = {
        "metadata": {
            "system_name": system_name,
            "config": config
        },
        "incentive_gap": gap_analysis,
        "conversion_obfuscation": conversion_analysis
    }
    
    # Save results
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"\nFriction Analysis Complete. Results saved to {args.output}")
    print(f"Required Cost: {required_cost}")
    print(f"Incentive Gap: {gap_analysis['ig']}")
    print(f"Closest Lower Pack: {gap_analysis['closest_lower_pack']}")
    print(f"Conversion Complexity Score: {conversion_analysis['conversion_complexity_score']}")
    print(f"Number of Exchange Steps: {conversion_analysis['num_exchange_steps']}")
    
    # Heuristic Conclusion
    if gap_analysis['ig'] > 0:
        print(f"\nConclusion: Player must buy multiple packs or overspend by {gap_analysis['ig']} units to meet the target.")
    if conversion_analysis['conversion_complexity_score'] > 2:
        print(f"Conclusion: High conversion complexity ({conversion_analysis['conversion_complexity_score']}) indicates significant financial obfuscation.")

if __name__ == "__main__":
    main()
