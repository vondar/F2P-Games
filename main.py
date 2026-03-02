import argparse
import sys
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="F2P Forensic Toolset - Unified Runner")
    subparsers = parser.add_subparsers(dest="command", help="Module to run")
    
    # Monetization Analysis
    monetization = subparsers.add_parser("monetization", help="Run monetization volatility analysis")
    monetization.add_argument("--config", type=str, required=True, help="Path to loot config")
    monetization.add_argument("--plot", action="store_true", help="Generate plots")
    monetization.add_argument("--report", action="store_true", help="Generate forensic report")
    
    # Retention Analysis
    retention = subparsers.add_parser("retention", help="Run retention rigidity analysis")
    retention.add_argument("--config", type=str, required=True, help="Path to retention config")
    retention.add_argument("--missed", type=int, default=1, help="Missed days to analyze")
    
    # Friction Analysis
    friction = subparsers.add_parser("friction", help="Run friction & obfuscation analysis")
    friction.add_argument("--config", type=str, required=True, help="Path to friction config")
    
    # Incentive Analysis
    incentives = subparsers.add_parser("incentives", help="Run retention-incentive curve analysis")
    incentives.add_argument("--simulate", action="store_true", help="Simulate data")
    
    # Audit
    audit = subparsers.add_parser("audit", help="Run SHA256 audit on ingestion directory")
    
    # State of the Tail (Big Three Audit)
    tail = subparsers.add_parser("state-of-the-tail", help="Generate 'State of the Tail' comparison for the Big Three")
    
    # Dashboard Launch
    dashboard = subparsers.add_parser("dashboard", help="Launch the Streamlit Forensic Dashboard")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return

    python_path = sys.executable
    project_root = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root
    
    try:
        if args.command == "monetization":
            cmd = [python_path, "src/run_analysis.py", "--config", args.config]
            if args.plot: cmd.append("--plot")
            if args.report: cmd.append("--report")
            subprocess.run(cmd, env=env, check=True)
            
        elif args.command == "dashboard":
            print("\nLaunching Streamlit Dashboard...")
            cmd = [python_path, "-m", "streamlit", "run", "src/app.py"]
            subprocess.run(cmd, env=env, check=True)
            
        elif args.command == "state-of-the-tail":
            configs = [
                "data/loot_configs/pubg_premium_crate.json",
                "data/loot_configs/bgmi_mythic_spin.json",
                "data/loot_configs/free_fire_diamond_royale.json"
            ]
            print("\n" + "="*50)
            print("GENERATING 'STATE OF THE TAIL' FORENSIC AUDIT")
            print("="*50 + "\n")
            for config in configs:
                if os.path.exists(config):
                    cmd = [python_path, "src/run_analysis.py", "--config", config, "--report"]
                    subprocess.run(cmd, env=env, check=True)
                else:
                    print(f"Warning: Config {config} not found. Skipping.")
            print("\nAudit Complete. Reports generated in data/results/")

        elif args.command == "retention":
            cmd = [python_path, "src/run_retention.py", "--config", args.config, "--missed_days", str(args.missed)]
            subprocess.run(cmd, env=env, check=True)
            
        elif args.command == "friction":
            cmd = [python_path, "src/run_friction.py", "--config", args.config]
            subprocess.run(cmd, env=env, check=True)
            
        elif args.command == "incentives":
            cmd = [python_path, "src/run_incentives.py"]
            if args.simulate: cmd.append("--simulate")
            subprocess.run(cmd, env=env, check=True)
            
        elif args.command == "audit":
            cmd = [python_path, "src/utils/audit.py"]
            subprocess.run(cmd, env=env, check=True)
            
    except subprocess.CalledProcessError as e:
        print(f"\n[FATAL] Module execution failed with exit code {e.returncode}")
        print(f"Command: {' '.join(e.cmd)}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"\n[FATAL] An unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
