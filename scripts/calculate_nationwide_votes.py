import json
from pathlib import Path
from typing import Dict, List, Any, Optional

def calculate_nationwide_votes():
    # Path to Data
    base_dir = Path("rawdata")
    pl_dir = base_dir / "pl"
    mp_dir = base_dir / "mp"
    
    pl_files = list(pl_dir.glob("*.json"))
    mp_files = list(mp_dir.glob("*.json"))
    
    if not pl_files:
        print("No data found in rawdata/pl/")
        return

    pl_party_votes: Dict[str, int] = {}  # party_code -> total_pl_votes
    mp_party_votes: Dict[str, int] = {}  # party_code -> total_mp_votes
    
    # 1. Calculate PL Votes
    print(f"Processing PL data from {len(pl_files)} files...")
    for file_path in pl_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data.get("entries", []):
                party_code = entry.get("partyCode")
                vote = int(entry.get("voteTotal", 0))
                if party_code:
                    pl_party_votes[party_code] = pl_party_votes.get(party_code, 0) + vote
        except Exception as e:
            print(f"Error processing PL {file_path}: {e}")

    # 2. Calculate MP Votes
    print(f"Processing MP data from {len(mp_files)} files...")
    for file_path in mp_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data.get("entries", []):
                party_code = entry.get("partyCode")
                vote = int(entry.get("voteTotal", 0))
                if party_code:
                    mp_party_votes[party_code] = mp_party_votes.get(party_code, 0) + vote
        except Exception as e:
            print(f"Error processing MP {file_path}: {e}")

    # Process results into groups
    group_a_stats = {"pl_votes": 0, "mp_votes": 0, "count": 0, "parties": []} # Lucky Number Candidate (1-15, excl 6,9,11)
    group_b_stats = {"pl_votes": 0, "mp_votes": 0, "count": 0, "parties": []} # Excluded (6, 9, 11)
    group_c_stats = {"pl_votes": 0, "mp_votes": 0, "count": 0, "parties": []} # Other Parties (16+)

    raw_list = []

    # Iterate over all parties found in PL (assuming PL covers all parties, valid assumption)
    all_party_codes = set(pl_party_votes.keys()) | set(mp_party_votes.keys())
    
    for party_code in all_party_codes:
        try:
            # Extract number
            if "-" in party_code:
                party_num = int(party_code.split("-")[-1])
            else:
                party_num = int(party_code)
        except ValueError:
            continue

        pl_total = pl_party_votes.get(party_code, 0)
        mp_total = mp_party_votes.get(party_code, 0)
        
        # Calculate Ratio (PL / MP). None when MP votes are 0 (ratio not meaningful)
        ratio = round(pl_total / mp_total, 2) if mp_total > 0 else None

        party_data = {
            "party_number": party_num,
            "party_code": party_code,
            "total_votes": pl_total, # Keep for backward compatibility with chart
            "pl_total_votes": pl_total,
            "mp_total_votes": mp_total,
            "ratio": ratio
        }
        raw_list.append(party_data)

        # Assign groups
        target_group = None
        if party_num in [6, 9, 11]:
            target_group = group_b_stats
        elif 1 <= party_num <= 15:
            target_group = group_a_stats
        elif party_num >= 16:
            target_group = group_c_stats
            
        if target_group:
            target_group["pl_votes"] += pl_total
            target_group["mp_votes"] += mp_total
            target_group["count"] += 1
            target_group["parties"].append(party_num)

    # Sort raw list
    raw_list.sort(key=lambda x: x["party_number"])

    # Output Results
    print("\n--- Nationwide Party Vote Analysis (MP vs PL) ---")
    
    def print_group(name, stats):
        print(f"\n{name}:")
        print(f"  Parties Included: {sorted(stats['parties'])}")
        print(f"  Total Parties: {stats['count']}")
        print(f"  Total PL Votes: {stats['pl_votes']:,}")
        print(f"  Total MP Votes: {stats['mp_votes']:,}")
        
        avg_pl = stats['pl_votes'] / stats['count'] if stats['count'] > 0 else 0
        ratio = stats['pl_votes'] / stats['mp_votes'] if stats['mp_votes'] > 0 else 0
        
        print(f"  Average PL Votes/Party: {avg_pl:,.2f}")
        print(f"  Group Ratio (PL/MP): {ratio:.2f}x")
        
        return {
            "pl_total": stats["pl_votes"],
            "mp_total": stats["mp_votes"],
            "average_pl": avg_pl,
            "ratio": ratio,
            "count": stats["count"]
        }

    res_a = print_group("Group A: Lucky Numbers (1-15, excl 6, 9, 11)", group_a_stats)
    res_b = print_group("Group B: Excluded (6, 9, 11)", group_b_stats)
    res_c = print_group("Group C: Other Parties (16+)", group_c_stats)

    # Creating a JSON output file for the user to use
    output_data = {
        "groups": {
            "A": res_a,
            "B": res_b,
            "C": res_c
        },
        "raw_parties": raw_list
    }
    
    output_file = "docs/data/nationwide_party_stats.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nDetailed stats saved to {output_file}")

if __name__ == "__main__":
    calculate_nationwide_votes()
