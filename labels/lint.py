import json
import logging
import sys
import argparse

# https://coolors.co/001219-005f73-0a9396-94d2bd-e9d8a6-ee9b00-ca6702-bb3e03-ae2012-9b2226
COLOR_SCHEME = [
    "001219",
    "005f73",
    "0a9396",
    "94d2bd",
    "e9d8a6",
    "ee9b00",
    "ca6702",
    "bb3e03",
    "ae2012",
    "9b2226",
]


def lint(fix: bool = True) -> bool:
    with open("labels.json") as f:
        content = f.read()

    try:
        decoded = json.loads(content)
    except Exception:
        logging.error("Invalid JSON: labels.json", exc_info=True)
        return False

    for label in decoded:
        if label["color"] not in COLOR_SCHEME:
            logging.error("Invalid color: %s", label["color"])
            return False

    new_content = json.dumps(decoded, indent=2, sort_keys=True)
    if fix:
        with open("labels.json", "w") as f:
            f.write(new_content)
    else:
        if content != new_content:
            logging.error("The JSON file: labels.json is not properly formatted")
            return False

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dont-fix",
        action="store_false",
        help="Don't try to fix the JSON file (lint mode)",
    )
    args = parser.parse_args()
    res = lint(not args.dont_fix)
    if not res:
        sys.exit(1)
