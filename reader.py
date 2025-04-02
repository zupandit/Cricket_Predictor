import json
import pandas as pd

# Load JSON data from file
with open("stat.json", "r") as file:
    data = json.load(file)

# Extract innings data
innings = data["innings"]

# Store overs with stats
all_over_stats = []

# Tracking cumulative stats
batter_stats = {}  # {"batter_name": {"runs": 0, "balls": 0}}
bowler_stats = {}  # {"bowler_name": {"runs_conceded": 0, "balls_bowled": 0}}
team_scores = {"New Zealand": 0, "India": 0}
total_overs = {"New Zealand": 0, "India": 0}
innings_targets = {inning["team"]: inning.get("target", {}).get("runs", None) for inning in innings}

# Define desirable score for the first innings
DESIRABLE_SCORE = 320

# Iterate through innings
for i, inning in enumerate(innings):
    team = inning["team"]
    target = innings_targets[team]  # Target for second innings
    total_balls = inning.get("target", {}).get("overs", 50) * 6  # Convert overs to balls
    desirable_target = DESIRABLE_SCORE if i == 0 else target  # First innings gets 320 as desirable target

    # Iterate through overs
    for over in inning["overs"]:
        over_number = over["over"]
        
        # Track over runs and wicket status
        over_runs = 0
        wicket_taken = 0  # Default to 0, will be set to 1 if a wicket falls

        # Process deliveries
        for delivery in over["deliveries"]:
            batter = delivery["batter"]
            bowler = delivery["bowler"]
            runs = delivery["runs"]["total"]
            
            # Update batter stats
            if batter not in batter_stats:
                batter_stats[batter] = {"runs": 0, "balls": 0}
            batter_stats[batter]["runs"] += delivery["runs"]["batter"]
            batter_stats[batter]["balls"] += 1

            # Update bowler stats
            if bowler not in bowler_stats:
                bowler_stats[bowler] = {"runs_conceded": 0, "balls_bowled": 0}
            bowler_stats[bowler]["runs_conceded"] += runs
            bowler_stats[bowler]["balls_bowled"] += 1

            # Update team score
            team_scores[team] += runs
            over_runs += runs

            # Check for wickets
            if "wickets" in delivery:
                wicket_taken = 1  # Mark that a wicket was taken in this over

        # Calculate stats
        batter_strike_rate = round((batter_stats[batter]["runs"] / batter_stats[batter]["balls"]) * 100, 2) if batter_stats[batter]["balls"] > 0 else 0
        bowler_economy = round((bowler_stats[bowler]["runs_conceded"] / (bowler_stats[bowler]["balls_bowled"] / 6)), 2) if bowler_stats[bowler]["balls_bowled"] > 0 else 0
        balls_remaining = total_balls - (total_overs[team] * 6 + len(over["deliveries"]))
        runs_needed = desirable_target - team_scores[team] if desirable_target else None
        desirable_run_rate = round((runs_needed / (balls_remaining / 6)), 2) if runs_needed is not None and balls_remaining > 0 else None

        # Store over stats
        all_over_stats.append({
            "team": team,
            "over": over_number,
            "batter": batter,
            "bowler": bowler,
            "batter_strike_rate": batter_strike_rate,
            "bowler_economy": bowler_economy,
            "desirable_run_rate": desirable_run_rate,
            "wicket_taken": wicket_taken
        })

        # Update total overs after processing an over
        total_overs[team] += 1

# Convert to DataFrame and display
df = pd.DataFrame(all_over_stats)
print(df)

# Optionally, save to CSV
df.to_csv("all_over_stats.csv", index=False)
