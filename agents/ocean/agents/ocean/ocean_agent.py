import json
import os


REQUIRED_FIELDS = [
    "parameter",
    "value",
    "unit",
    "latitude",
    "longitude",
    "timestamp",
    "source",
    "confidence"
]


def normalize_observation(observation):

    return {
        "parameter": observation["parameter"],
        "value": observation["value"],
        "unit": observation["unit"],
        "latitude": observation["latitude"],
        "longitude": observation["longitude"],
        "timestamp": observation["timestamp"],
        "source": observation["source"],
        "confidence": observation["confidence"]
    }


def validate_observation(observation):

    for field in REQUIRED_FIELDS:

        if field not in observation:
            return False

        if observation[field] is None:
            return False

    return True


def get_marine_data():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    data_path = os.path.join(
        base_dir,
        "../../data/sample/marine_data.json"
    )

    with open(data_path, "r") as file:
        raw_data = json.load(file)

    marine_data = []

    for observation in raw_data:

        normalized = normalize_observation(observation)

        if validate_observation(normalized):
            marine_data.append(normalized)

    return marine_data


if __name__ == "__main__":

    data = get_marine_data()

    print("\nORCA MARINE INTELLIGENCE AGENT\n")

    for observation in data:
        print(
            observation["parameter"],
            ":",
            observation["value"],
            observation["unit"]
        )
