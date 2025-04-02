import os
import json
import shutil

# CONFIGURABLE PATHS
SOURCE_FOLDER = "./all_matches"         # folder with 5000 jsons
DEST_FOLDER = "./filtered_matches"      # new folder for filtered files

# Top cricket teams (edit or add more as needed)
TOP_TEAMS = {
    "Pakistan", "India", "Australia", "New Zealand", "England",
    "Bangladesh", "Sri Lanka", "West Indies", "South Africa", "Netherlands",
    "Afghanistan", "Ireland"
}

def match_is_valid(match_data):
    try:
        # Check for male gender
        if match_data["info"].get("gender") != "male":
            return False

        # Check if either team is in the top teams list
        teams = match_data["info"].get("teams", [])
        return any(team in TOP_TEAMS for team in teams)
    except Exception as e:
        print("Error checking file:", e)
        return False

def main():
    if not os.path.exists(DEST_FOLDER):
        os.makedirs(DEST_FOLDER)

    count = 0
    for filename in os.listdir(SOURCE_FOLDER):
        if filename.endswith(".json"):
            file_path = os.path.join(SOURCE_FOLDER, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if match_is_valid(data):
                    shutil.copy(file_path, os.path.join(DEST_FOLDER, filename))
                    count += 1

            except Exception as e:
                print(f"Skipping {filename} due to error: {e}")

    print(f"Filtered and copied {count} files to '{DEST_FOLDER}'.")

if __name__ == "__main__":
    main()
