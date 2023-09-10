import numpy as np
from typing import Tuple, List


class Model:
    def trend(
        self, type: str, a: float, b: float, N: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        time_values = np.arange(0, N)

        trend_dict = {
            "Линейно восходящий тренд": a * time_values + b,
            "Линейно нисходящий тренд": -a * time_values + b,
            "Нелинейно восходящий тренд": b * np.exp(a * time_values),
            "Нелинейно нисходящий тренд": b * np.exp(-a * time_values),
        }

        trend_values = trend_dict.get(type)
        return time_values, trend_values

    def combined_trend(
        self, types: List[str], a: int, b: int, N: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        time_values = np.arange(0, N)
        combined_trend_values = np.zeros(N)

        if len(types) == 0:
            return np.array([0]), np.array([0])

        combined_trend_values = np.array_split(combined_trend_values, len(types))

        for i, trend_type in enumerate(types):
            _, trend_values = self.trend(
                trend_type, a, b, len(combined_trend_values[i])
            )
            combined_trend_values[i] += trend_values

        return time_values, np.concatenate(combined_trend_values, axis=0)
