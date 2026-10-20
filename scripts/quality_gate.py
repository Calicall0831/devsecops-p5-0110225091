"""Quality Gate: gagalkan pipeline bila temuan Bandit melewati ambang batas."""
import json
import sys

MAX_HIGH = 0
MAX_MEDIUM = 0

with open(sys.argv[1], encoding="utf-8") as f:
    report = json.load(f)

counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
for issue in report.get("results", []):
    counts[issue["issue_severity"]] += 1

print(f"Temuan SAST -> HIGH: {counts['HIGH']}, MEDIUM: {counts['MEDIUM']}, LOW: {counts['LOW']}")
print(f"Ambang batas -> HIGH <= {MAX_HIGH}, MEDIUM <= {MAX_MEDIUM}")

if counts["HIGH"] > MAX_HIGH or counts["MEDIUM"] > MAX_MEDIUM:
    print("QUALITY GATE: FAILED")
    sys.exit(1)
print("QUALITY GATE: PASSED")
