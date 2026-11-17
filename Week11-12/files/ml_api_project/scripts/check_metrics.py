"""Quality gate: exit 1 if the model is worse than the threshold.

Run:  python scripts/check_metrics.py --min-auc 0.75
"""

import argparse
import json
import sys
from pathlib import Path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", default="models/metrics.json")
    parser.add_argument("--min-auc", type=float, default=0.75)
    args = parser.parse_args(argv)

    path = Path(args.metrics)
    if not path.exists():
        print(f"metrics file not found: {path}")
        return 2
    auc = json.loads(path.read_text())["auc"]
    if auc < args.min_auc:
        print(f"FAIL: AUC {auc} is below the minimum {args.min_auc}")
        return 1
    print(f"OK: AUC {auc} >= {args.min_auc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
