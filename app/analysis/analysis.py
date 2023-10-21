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

    def stationarity(self, data: np.ndarray, M: int) -> bool:
        intervals = [
            {
                "Среднее значение": np.mean(segment),
                "Стандартное отклонение": np.std(segment),
            }
            for segment in np.array_split(data, M)
        ]

        for i in range(M - 1):
            j = i + 1
            abs_diff_mean = np.abs(
                intervals[i]["Среднее значение"] - intervals[j]["Среднее значение"]
            )
            abs_diff_std = np.abs(
                intervals[i]["Стандартное отклонение"]
                - intervals[j]["Стандартное отклонение"]
            )

            if (
                abs_diff_mean / intervals[i]["Среднее значение"] * 100 >= 5
                or abs_diff_std / intervals[i]["Стандартное отклонение"] * 100 >= 5
            ):
                return "Процесс не стационарный"

        return "Процесс стационарный"
