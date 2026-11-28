import json

from scripts.check_metrics import main


def write_metrics(tmp_path, auc):
    path = tmp_path / "metrics.json"
    path.write_text(json.dumps({"auc": auc}))
    return str(path)


def test_passes_when_auc_is_high_enough(tmp_path):
    assert main(["--metrics", write_metrics(tmp_path, 0.8), "--min-auc", "0.75"]) == 0


def test_fails_when_auc_is_too_low(tmp_path):
    assert main(["--metrics", write_metrics(tmp_path, 0.6), "--min-auc", "0.75"]) == 1


def test_missing_file_is_an_error(tmp_path):
    assert main(["--metrics", str(tmp_path / "nope.json")]) == 2
