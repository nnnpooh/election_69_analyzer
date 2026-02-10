import json
from pathlib import Path
from typing import List, Dict, Any

def compare_mp_and_pl() -> None:
    """
    Compares the winning MP candidate number with the top 20 Party List party numbers.
    """
    base_dir = Path("rawdata")
    mp_dir = base_dir / "mp"
    pl_dir = base_dir / "pl"
    
    if not mp_dir.exists() or not pl_dir.exists():
        print("Error: rawdata/mp or rawdata/pl directory not found.")
        return

    mp_files = sorted([f for f in mp_dir.iterdir() if f.suffix == ".json"])
    
    print(f"{'Area':<6} | {'MP Num':<6} | {'MP Party':<10} | {'Status':<30}")
    print("-" * 50)

    all_matches: List[Dict[str, Any]] = []

    for mp_path in mp_files:
        area_code = mp_path.stem
        pl_path = pl_dir / mp_path.name
        
        if not pl_path.exists():
            continue

        try:
            # 1. Get MP winning info
            with open(mp_path, "r", encoding="utf-8") as f:
                mp_data = json.load(f)
            
            mp_entries = mp_data.get("entries", [])
            if not mp_entries:
                continue
                
            top_mp = mp_entries[0]
            winning_candidate = top_mp.get("candidateCode", "")
            mp_party = top_mp.get("partyCode", "Unknown") # Get party of the MP
            
            # Extraction logic: CANDIDATE-MP-100105 -> 05
            prefix = f"CANDIDATE-MP-{area_code}"
            mp_number = winning_candidate[len(prefix):] if winning_candidate.startswith(prefix) else None
            
            if not mp_number:
                continue

            # 2. Get Top 20 Party List data
            with open(pl_path, "r", encoding="utf-8") as f:
                pl_data = json.load(f)
                
            pl_entries = pl_data.get("entries", [])[:20] # Get rank 1 to 20
            
            matches = []
            for pl_entry in pl_entries:
                pl_party_code = pl_entry.get("partyCode", "")
                last_2 = pl_party_code[-2:]
                
                # Logic: Skip if party number is "6", "9" or "11"
                # "6" is United Thai Nation Party
                # "9" is Pheu Thai Party
                # "11" is Chart Thai Pattana Party
                if last_2 in ["06", "09", "11"]:
                    continue
                
                # Compare
                if last_2 == mp_number:
                    match_info = {
                        "area": area_code,
                        "mp_number": mp_number,
                        "mp_party": mp_party,
                        "pl_rank": pl_entry.get('rank'),
                        "pl_party_code": pl_party_code
                    }
                    matches.append(f"Rank {match_info['pl_rank']} (Party List {last_2})")
                    all_matches.append(match_info)

            # 3. Output Row
            if matches:
                status = "MATCH: " + ", ".join(matches)
            else:
                status = "No Match"
                
            print(f"{area_code:<6} | {mp_number:<6} | {mp_party:<10} | {status}")

        except Exception as e:
            print(f"Error processing {area_code}: {e}")

    # Final Summary (Counting and Sorting)
    print("\n" + "="*40)
    print(f"{'SUMMARY BY PARTY (DESC)':^40}")
    print("="*40)
    
    if not all_matches:
        print("No matches discovered.")
    else:
        # Count matches per party
        party_counts = {}
        for m in all_matches:
            p = m['mp_party']
            party_counts[p] = party_counts.get(p, 0) + 1
            
        # Sort desc
        sorted_parties = sorted(party_counts.items(), key=lambda item: item[1], reverse=True)
        
        print(f"{'Party Code':<20} | {'Match Count':<10}")
        print("-" * 40)
        for party, count in sorted_parties:
            print(f"{party:<20} | {count:<10}")
    print("="*40)

if __name__ == "__main__":
    print("--- MP winning number vs Top 20 Party List comparison ---")
    print("Logic: Ignores Party 06, 09 and 11")
    compare_mp_and_pl()
