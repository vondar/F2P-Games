import argparse
import os
import json
from src.utils.config_loader import load_retention_config
from src.metrics.retention import calculate_retention_rigidity, calculate_schedule_rigidity

def main():
    parser = argparse.ArgumentParser(description="F2P Retention Analysis Runner")
    parser.add_argument("--config", type=str, required=True, help="Path to retention configuration JSON")
    parser.add_argument("--missed_days", type=int, default=1, help="Number of days missed to analyze debt")
    parser.add_argument("--output", type=str, default="data/results/retention_analysis.json", help="Path to output results")
    
    args = parser.parse_args()
    
    print(f"Loading retention config from {args.config}...")
    config = load_retention_config(args.config)
    
    season_name = config.get("season_name", "Unknown Season")
    total_xp = config.get("total_xp_required", 10000)
    daily_xp = config.get("daily_free_xp", 100)
    weekly_xp = config.get("weekly_free_xp", 500)
    duration = config.get("season_duration_days", 60)
    login_windows = config.get("login_windows", [])
    
    # Calculate daily average required progress
    # (Total XP - Weekly XP contribution) / Duration
    num_weeks = duration / 7
    total_weekly_xp = num_weeks * weekly_xp
    required_daily_xp = (total_xp - total_weekly_xp) / duration
    
    # 1. Retention Rigidity (Digital Debt)
    # Missed progress = required daily xp * missed days
    missed_progress = required_daily_xp * args.missed_days
    # Recovery progress is what's left over from daily_xp after doing daily requirements
    # If required_daily_xp >= daily_xp, recovery is impossible (interest -> infinity)
    daily_recoverable_progress = daily_xp - required_daily_xp
    
    print(f"Analyzing '{season_name}' for {args.missed_days} missed day(s)...")
    
    if daily_recoverable_progress <= 0:
        print("Warning: Required daily progress exceeds daily limit. Recovery is impossible!")
        rigidity = {
            "oca": float('inf'),
            "recovery_interest_rate": float('inf')
        }
    else:
        rigidity = calculate_retention_rigidity(missed_progress, daily_recoverable_progress)
        
    # 2. Schedule Rigidity (SRI)
    windows = [(w['start'], w['end']) for w in login_windows]
    schedule = calculate_schedule_rigidity(windows)
    
    results = {
        "metadata": {
            "season_name": season_name,
            "missed_days": args.missed_days,
            "config": config
        },
        "retention_rigidity": rigidity,
        "schedule_rigidity": schedule
    }
    
    # Save results
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"\nRetention Analysis Complete. Results saved to {args.output}")
    print(f"OCA (Opportunity Cost of Absence): {rigidity['oca']:.2f}")
    if rigidity['recovery_interest_rate'] != float('inf'):
        print(f"Recovery Interest Rate: {rigidity['recovery_interest_rate']:.1f}%")
    print(f"Schedule Rigidity Index (SRI): {schedule['sri']:.2f}")
    print(f"Number of login windows: {schedule['num_windows']}")

if __name__ == "__main__":
    main()
