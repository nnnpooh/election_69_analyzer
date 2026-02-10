import sys
import subprocess
from pathlib import Path

def run_script(script_name: str) -> None:
    script_path = Path("scripts") / script_name
    print(f"\n--- Running {script_name} ---")
    result = subprocess.run([sys.executable, str(script_path)])
    if result.returncode != 0:
        print(f"Error running {script_name}")
        sys.exit(result.returncode)

def main() -> None:
    print("Election 69 Analyzer CLI")
    print("=" * 30)
    print("1. Scrape Data (election_scraper.py)")
    print("2. Analyze Anomalies (generate_anomaly_report.py)")
    print("3. Calculate Nationwide Votes (calculate_nationwide_votes.py)")
    print("4. Compare MP/PL (mp_pl_comparer.py) - Legacy")
    print("5. Run Full Analysis Pipeline (2 -> 3)")
    print("q. Quit")
    
    choice = input("\nSelect an option: ").strip().lower()
    
    if choice == "1":
        run_script("election_scraper.py")
    elif choice == "2":
        run_script("generate_anomaly_report.py")
    elif choice == "3":
        run_script("calculate_nationwide_votes.py")
    elif choice == "4":
        run_script("mp_pl_comparer.py")
    elif choice == "5":
        run_script("generate_anomaly_report.py")
        run_script("calculate_nationwide_votes.py")
    elif choice == "q":
        print("Exiting.")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
