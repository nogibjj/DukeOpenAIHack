import json


def validate_json(filename):
    with open(filename, "r") as f:
        for i, line in enumerate(f, 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON on line {i}: {e}")


# Use the function to validate your JSON file
validate_json("play_by_play.json")
