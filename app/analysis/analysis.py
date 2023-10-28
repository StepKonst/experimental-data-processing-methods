__all__ = ["Analysis"]

import numpy as np
import pandas as pd
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

    def hist(self, data: np.ndarray, M: int) -> np.ndarray:
        hist, bins = np.histogram(data, M, density=True)
        bin_center = (bins[:-1] + bins[1:]) / 2

        return pd.DataFrame({"x": bin_center, "y": hist})

    def acf(self, data: np.ndarray, function_type: str) -> list:
        data_mean = np.mean(data)
        n = len(data)
        l_values = np.arange(0, n)
        ac_values = []

        for L in l_values:
            numerator = np.sum(
                (data[: n - L - 1] - data_mean) * (data[L : n - 1] - data_mean)
            )
            denominator = np.sum((data - data_mean) ** 2)

            if function_type == "Автокорреляционная функция":
                ac = numerator / denominator
            elif function_type == "Ковариационная функция":
                ac = numerator / n

            ac_values.append(ac)

        return pd.DataFrame({"L": l_values, "AC": ac_values})

    def ccf(self, datax: np.ndarray, datay: np.ndarray):
        if len(datax) != len(datay):
            raise ValueError("Длины входных данных не совпадают")

        n = len(datax)
        l_values = np.arange(0, n)
        x_mean = np.mean(datax)
        y_mean = np.mean(datay)
        ccf_values = np.correlate(datax - x_mean, datay - y_mean, mode="full") / n

        return pd.DataFrame({"L": l_values, "CCF": ccf_values[:n]})
