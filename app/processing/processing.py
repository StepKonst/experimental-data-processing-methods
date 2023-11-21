__all__ = ["Processing"]

import numpy as np


class Processing:
    def antishift(self, data: np.ndarray) -> np.ndarray:
        mean_data = np.mean(data)
        antishift_data = data - mean_data

        return antishift_data

    def antispike(self, data: np.ndarray, R: float) -> np.ndarray:
        n = len(data)

        for i in range(1, n - 1):
            if abs(data[i] - data[i - 1]) > R and abs(data[i] - data[i + 1]) > R:
                data[i] = (data[i - 1] + data[i + 1]) / 2

        return data

    def antitrendlinear(self, data: np.ndarray) -> np.ndarray:
        diff_data = np.diff(data)

        return diff_data

    def antitrendnonlinear(self, data: np.ndarray, W: int) -> np.ndarray:
        N = len(data) - W
        for n in range(N):
            data[n] -= sum(data[n : n + W]) / W

        return data
