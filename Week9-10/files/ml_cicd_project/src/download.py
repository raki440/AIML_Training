"""Download or copy a model to a specified destination."""

import argparse
import shutil
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


def download_model(source: str, destination: str) -> Path:
    parsed_url = urlparse(source)

    if parsed_url.scheme in ("http", "https"):
        filename = Path(parsed_url.path).name or "model.joblib"
    else:
        source_path = Path(source)
        if not source_path.is_file():
            raise FileNotFoundError(f"Model source not found: {source}")
        filename = source_path.name

    destination_path = Path(destination)
    destination_path.mkdir(parents=True, exist_ok=True)
    output_path = destination_path / filename

    if parsed_url.scheme in ("http", "https"):
        with urlopen(source, timeout=60) as response:
            with output_path.open("wb") as output:
                shutil.copyfileobj(response, output)
    else:
        shutil.copy2(source_path, output_path)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Download a trained ML model")
    parser.add_argument("--source", required=True, help="Local model path or URL")
    parser.add_argument("--destination", required=True, help="Destination folder")
    args = parser.parse_args()

    saved_path = download_model(args.source, args.destination)
    print(f"Model downloaded successfully: {saved_path}")


if __name__ == "__main__":
    main()
