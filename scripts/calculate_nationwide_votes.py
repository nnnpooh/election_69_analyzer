import json
import glob
import os

def calculate_nationwide_votes():
    # Path to PL data
    pl_files = glob.glob(os.path.join("data", "pl", "*.json"))
    
    if not pl_files:
        print("No data found in data/pl/")
        return

    party_votes = {}  # party_code -> total_votes
    
    print(f"Processing {len(pl_files)} files...")

    for file_path in pl_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            entries = data.get("entries", [])
            if not entries:
                continue
                
            for entry in entries:
                party_code = entry.get("partyCode")
                vote_total = entry.get("voteTotal", 0)
                
                # voteTotal comes as int based on typical JSON but let's be safe
                if isinstance(vote_total, str):
                    vote_total = int(vote_total)
                
                if party_code:
                    party_votes[party_code] = party_votes.get(party_code, 0) + vote_total

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Process results into groups
    group_a_stats = {"total_votes": 0, "count": 0, "parties": []} # Lucky Number Candidate (1-15, excl 6,9)
    group_b_stats = {"total_votes": 0, "count": 0, "parties": []} # Excluded (6, 9)
    group_c_stats = {"total_votes": 0, "count": 0, "parties": []} # Other Parties (16+)

    raw_list = []

    # Sort by party number for cleaner processing
    # Assuming format PARTY-XXXX or similar where suffix is number
    # If key is simple number string, handle that too
    
    for party_code, total_votes in party_votes.items():
        try:
            # Extract number. partyCode format is likely "PARTY-0001"
            # It might handle different formats if necessary, but assuming "PARTY-" prefix or simple int
            if "-" in party_code:
                party_num = int(party_code.split("-")[-1])
            else:
                party_num = int(party_code)
        except ValueError:
            print(f"Skipping invalid party code format: {party_code}")
            continue

        party_data = {
            "party_number": party_num,
            "party_code": party_code,
            "total_votes": total_votes
        }
        raw_list.append(party_data)

        # Assign groups
        if party_num in [6, 9]:
            group_b_stats["total_votes"] += total_votes
            group_b_stats["count"] += 1
            group_b_stats["parties"].append(party_num)
        elif 1 <= party_num <= 15:
            group_a_stats["total_votes"] += total_votes
            group_a_stats["count"] += 1
            group_a_stats["parties"].append(party_num)
        elif party_num >= 16:
            group_c_stats["total_votes"] += total_votes
            group_c_stats["count"] += 1
            group_c_stats["parties"].append(party_num)

    # Sort raw list
    raw_list.sort(key=lambda x: x["party_number"])

    # Output Results
    print("\n--- Nationwide Party Vote Analysis ---")
    
    def print_group(name, stats):
        avg = stats["total_votes"] / stats["count"] if stats["count"] > 0 else 0
        print(f"\n{name}:")
        print(f"  Parties Included: {sorted(stats['parties'])}")
        print(f"  Total Parties: {stats['count']}")
        print(f"  Total Votes: {stats['total_votes']:,}")
        print(f"  Average Votes/Party: {avg:,.2f}")
        return {"total": stats["total_votes"], "average": avg, "count": stats["count"]}

    res_a = print_group("Group A: Lucky Numbers (1-15, excl 6, 9)", group_a_stats)
    res_b = print_group("Group B: Excluded (6, 9)", group_b_stats)
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
    
    output_file = "data/nationwide_party_stats.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nDetailed stats saved to {output_file}")

if __name__ == "__main__":
    calculate_nationwide_votes()
