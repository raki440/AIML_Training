"""Send requests and count which server instance answered (X-Served-By header).

Run:  python scripts/load_demo.py --url http://localhost:8080 --n 30
"""

import argparse
import collections
import json
import urllib.request

SAMPLE = {
    "tenure_months": 3,
    "monthly_charges": 95,
    "logins_per_week": 1,
    "support_tickets": 4,
    "plan": "basic",
}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8080")
    parser.add_argument("--n", type=int, default=30)
    args = parser.parse_args(argv)

    counts = collections.Counter()
    body = json.dumps(SAMPLE).encode()
    for _ in range(args.n):
        request = urllib.request.Request(
            f"{args.url}/v1/predict", data=body, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(request) as response:
            counts[response.headers.get("X-Served-By", "unknown")] += 1
            response.read()
    for host, count in counts.most_common():
        print(f"{host}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
