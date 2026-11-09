#Standardize only the second column of data.

import numpy as np
from mlkit.utils import set_seed

rng = set_seed(42)

data = rng.normal([50, 70], [10, 20], size=(5, 2))

second_column = data[:, 1]

scaled_second = (
    second_column - second_column.mean()
) / second_column.std()

print(scaled_second.round(2))
print("Mean:", scaled_second.mean().round(6))
print("Standard deviation:", scaled_second.std().round(6))

print("=========================================")

# Count how many charges values are above the mean (ignore NaN)
charges = np.array([55.0, 72.5, np.nan, 130.0, 61.2])

mean_charges = np.nanmean(charges)

count = np.sum(charges > mean_charges)

print("Mean charges:", mean_charges)
print("Count above mean:", count)


print("=========================================")

#Time np.mean against a Python loop on 10 million numbers.
import time
import numpy as np

numbers = np.arange(10_000_000)

# Python loop
t = time.perf_counter()

total = 0
for num in numbers:
    total += num

python_mean = total / len(numbers)

loop_time = time.perf_counter() - t

# NumPy mean
t = time.perf_counter()

numpy_mean = np.mean(numbers)

numpy_time = time.perf_counter() - t

print("Python mean:", python_mean)
print("NumPy mean:", numpy_mean)

print(
    f"Python loop: {loop_time:.3f}s | "
    f"NumPy: {numpy_time:.4f}s"
)