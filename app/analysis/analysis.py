__all__ = ["Analysis"]

import numpy as np
from scipy.stats import kurtosis, skew


class Analysis:
    def statistics(self, N: int, data: np.ndarray) -> dict:
        return {
            "Минимальное значение": np.min(data),
            "Максимальное значение": np.max(data),
            "Среднее значение": np.mean(data),
            "Дисперсия": np.var(data),
            "Стандартное отклонение": np.std(data),
            "Ассиметрия": skew(data),
            "Коэффициент ассиметрии": skew(data) / np.std(data),
            "Эксцесс": kurtosis(
                data, fisher=False
            ),  # Эксцесс sum((x - mean_value) ** 4 for x in data)
            "Куртозис": kurtosis(data, fisher=True),
            "Средний квадрат": np.mean(data**2),
            "Среднеквадратическая ошибка": np.sqrt(np.mean(data**2)),
        }

    def stationarity(self, data: np.ndarray, M: int) -> str:
        data = abs(data)
        segments = np.array_split(data, M)
        means = [np.mean(segment) for segment in segments]
        stds = [np.std(segment) for segment in segments]

        for i in range(M - 1):
            abs_diff_mean = np.abs(means[i + 1] - means[i])
            abs_diff_std = np.abs(stds[i + 1] - stds[i])

            if abs_diff_mean / means[i] >= 0.05 or abs_diff_std / stds[i] >= 0.05:
                return "Процесс нестационарный"

        return "Процесс стационарный"
