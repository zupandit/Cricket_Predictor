import os
import json
import pandas as pd

MATCH_DIR = "./filtered_matches"
OUTPUT_CSV = "over_features.csv"

def get_over_wickets(over):
    wickets = 0
    for ball in over.get("deliveries", []):
        if "wickets" in ball:
            wickets += len(ball["wickets"])
    return wickets

def calculate_striker_stats(over_history, striker):
    runs = 0
    balls = 0
    boundaries = 0
    for over in over_history:
        for ball in over.get("deliveries", []):
            if ball.get("batter") == striker:
                runs += ball.get("runs", {}).get("batter", 0)
                balls += 1
                if ball.get("runs", {}).get("batter", 0) in [4, 6]:
                    boundaries += 1
    strike_rate = (runs / balls * 100) if balls > 0 else 0
    return balls, strike_rate, boundaries

def calculate_dot_ball_pressure(over_history):
    dot_balls = 0
    total_balls = 0
    for over in over_history[-2:]:
        for ball in over.get("deliveries", []):
            total_balls += 1
            if ball.get("runs", {}).get("total", 0) == 0:
                dot_balls += 1
    return (dot_balls / total_balls * 100) if total_balls > 0 else 0

def calculate_bowler_stats(over_history, bowler):
    runs = 0
    balls = 0
    wickets = 0
    for over in over_history:
        for ball in over.get("deliveries", []):
            if ball.get("bowler") == bowler:
                balls += 1
                runs += ball.get("runs", {}).get("total", 0)
                if "wickets" in ball:
                    wickets += len(ball["wickets"])
    economy = (runs / (balls / 6)) if balls > 0 else 0
    return economy, wickets

def count_wickets_since(over_wickets, current):
    for i in range(current - 1, -1, -1):
        if over_wickets[i] > 0:
            return current - i
    return current + 1

def count_wickets_last_n_overs(over_wickets, current, n):
    return sum(over_wickets[max(0, current - n):current])

def count_boundaries_last_n_overs(overs_data, current, n):
    boundaries = 0
    for i in range(max(0, current - n), current):
        for ball in overs_data[i].get("deliveries", []):
            if ball.get("runs", {}).get("batter", 0) in [4, 6]:
                boundaries += 1
    return boundaries

def count_dots_last_over(overs_data, current):
    if current == 0:
        return 0
    dots = 0
    for ball in overs_data[current - 1].get("deliveries", []):
        if ball.get("runs", {}).get("total", 0) == 0:
            dots += 1
    return dots

def calculate_required_minus_desired(current_runs, balls_faced, target):
    overs_faced = balls_faced / 6
    current_rr = current_runs / overs_faced if overs_faced > 0 else 0
    desired_rr = target / 20
    required = (target - current_runs) / ((120 - balls_faced) / 6) if balls_faced < 120 and current_runs < target else 0
    return required - desired_rr

def determine_match_phase(over_num):
    if over_num < 6:
        return "Powerplay"
    elif over_num < 15:
        return "Middle"
    else:
        return "Death"

def extract_features(match_path):
    try:
        with open(match_path) as f:
            data = json.load(f)

        features = []
        innings_list = data["innings"]

        for inn_idx, innings in enumerate(innings_list):
            team = innings["team"]
            overs_data = innings["overs"]
            over_wickets = []
            total_runs = 0
            balls_faced = 0
            striker = None
            bowler_stats = {}

            for over_index, over in enumerate(overs_data):
                over_wickets.append(get_over_wickets(over))

            for over_index, over in enumerate(overs_data):
                if over_index + 1 >= len(overs_data):
                    continue

                next_over = overs_data[over_index + 1]
                next_wicket = get_over_wickets(next_over)
                wicket_next_over = 1 if next_wicket > 0 else 0

                striker = over["deliveries"][0].get("batter")
                bowler = over["deliveries"][0].get("bowler")

                past_overs = overs_data[:over_index + 1]

                balls_faced_by_striker, striker_sr, striker_boundaries = calculate_striker_stats(past_overs, striker)
                dot_pressure = calculate_dot_ball_pressure(past_overs)
                economy, bowler_wickets = calculate_bowler_stats(past_overs, bowler)

                overs_completed = over_index + 1
                overs_since_wicket = count_wickets_since(over_wickets, over_index)
                total_wickets = sum(over_wickets[:over_index + 1])
                current_rr = (total_runs / overs_completed) if overs_completed > 0 else 0
                req_minus_desired = calculate_required_minus_desired(total_runs, balls_faced, 180)

                wkts_last_3 = count_wickets_last_n_overs(over_wickets, over_index, 3)
                boundaries_last_3 = count_boundaries_last_n_overs(overs_data, over_index, 3)
                dots_last_over = count_dots_last_over(overs_data, over_index)
                pplay_remaining = max(0, 6 - (over_index + 1))
                match_phase = determine_match_phase(over_index)

                for ball in over["deliveries"]:
                    total_runs += ball.get("runs", {}).get("total", 0)
                    balls_faced += 1

                features.append({
                    "match_id": os.path.basename(match_path),
                    "innings": inn_idx,
                    "team": team,
                    "over": over_index,
                    "balls_faced_by_striker": balls_faced_by_striker,
                    "striker_strike_rate": striker_sr,
                    "striker_boundaries_hit": striker_boundaries,
                    "dot_ball_pressure": dot_pressure,
                    "current_bowler_economy": economy,
                    "bowler_wickets_in_match": bowler_wickets,
                    "total_overs_completed": overs_completed,
                    "overs_since_last_wicket": overs_since_wicket,
                    "number_of_wickets_lost": total_wickets,
                    "required_desired_run_rate": req_minus_desired,
                    "current_run_rate": current_rr,
                    "wickets_lost_last_3_overs": wkts_last_3,
                    "number_of_boundaries_last_3_overs": boundaries_last_3,
                    "number_of_dot_balls_last_over": dots_last_over,
                    "powerplay_overs_remaining": pplay_remaining,
                    "match_phase": match_phase,
                    "wicket_next_over": wicket_next_over,
                })

        return features
    except Exception as e:
        print(f"Error processing {os.path.basename(match_path)}: {e}")
        return []

def main():
    all_features = []
    print("\n🚀 Starting feature extraction from JSON matches")

    for fname in os.listdir(MATCH_DIR):
        if fname.endswith(".json"):
            full_path = os.path.join(MATCH_DIR, fname)
            print(f"\n🔍 Processing {full_path}")
            feats = extract_features(full_path)
            all_features.extend(feats)

    df = pd.DataFrame(all_features)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"\n📊 Total extracted rows: {len(df)}")
    print(f"✅ Extracted features saved to {OUTPUT_CSV}\n")

if __name__ == "__main__":
    main()
