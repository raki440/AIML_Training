import pytest

from src.predict import SAMPLES, predict
from src.train import MODEL_FILE, train


def test_train_saves_model_and_predicts(tmp_path):
    info = train(tmp_path)
    assert (tmp_path / MODEL_FILE).exists() and info["auc"] > 0.7
    risky, loyal = predict(SAMPLES, tmp_path)
    assert 0 <= loyal < risky <= 1


def test_missing_model_gives_clear_message(tmp_path):
    with pytest.raises(SystemExit) as e:
        predict(SAMPLES, tmp_path)
    assert "Run training first" in str(e.value)


def test_train_writes_metrics_file(tmp_path):
    from src.train import METRICS_FILE

    train(tmp_path)
    assert (tmp_path / METRICS_FILE).exists()
