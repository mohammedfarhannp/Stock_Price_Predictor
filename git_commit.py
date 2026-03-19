import os

Commands = [
    "git add data\\raw\\ROLEXRINGS_NS_01-01-2025_to_CURRENT.csv",
    "git commit -m \"New Data Added!\" -m \"Automated Commit!\"",
    "git add data\\processed\\processed_data.csv",
    "git commit -m \"New Processed Data!\" -m \"Automated Commit!\"",
    "git add data\\prediction\\predictions.csv",
    "git commit -m \"New Prediction Added!\" -m \"Automated Commit!\"",
    "git add models\\best_model.pkl",
    "git commit -m \"Model Updated!\" -m \"Automated Commit!\"",
    "git add .",
    "git commit -m \"New Data Added!\" -m \"Automated Commit!\""
]

for command in Commands:
    os.system(command)