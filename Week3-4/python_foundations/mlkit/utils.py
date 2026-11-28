import random

import numpy as np

from mlkit.config import SEED


def set_seed(seed: int = SEED) -> np.random.Generator:
    """Seed Python and NumPy, and return a NumPy Generator for new code."""
    random.seed(seed)
    np.random.seed(seed)
    return np.random.default_rng(seed)
