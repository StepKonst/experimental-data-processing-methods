__all__ = ["Model"]

import random
from typing import List, Tuple

import numpy as np


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
            return None, None

        combined_trend_values = np.array_split(combined_trend_values, len(types))

        for i, trend_type in enumerate(types):
            _, trend_values = self.trend(
                trend_type, a, b, len(combined_trend_values[i])
            )
            combined_trend_values[i] += trend_values

        return time_values, np.concatenate(combined_trend_values)

    def noise(self, N: int, R: float) -> Tuple[np.ndarray, np.ndarray]:
        time_values = np.arange(0, N)
        noise_values = np.random.uniform(-R, R, size=N)

        x_min = np.min(noise_values)
        x_max = np.max(noise_values)

        data = ((noise_values - x_min) / (x_max - x_min) - 0.5) * 2 * R

        return time_values, data

    def my_noise(self, N: int, R: float) -> Tuple[np.ndarray, np.ndarray]:
        time_values = np.arange(0, N)
        noise_values = np.array([random.random() * 2 - 1 for _ in range(N)]) * R
        data = noise_values

        return time_values, data

    def shift(self, inData: np.ndarray, C: float, N1: int, N2: int) -> np.ndarray:
        inData[N1:N2] += C
        return inData

    def spikes(self, N: int, M: int, R: float, Rs: float) -> Tuple[np.ndarray, dict]:
        data = np.zeros(N + 1)
        positions = random.sample(range(N), M)
        values_emissions_plus = np.random.uniform(R - Rs, R + Rs, size=M)
        values_emissions_minus = np.random.uniform(-R - Rs, -R + Rs, size=M)
        values_emissions = np.concatenate(
            [values_emissions_plus, values_emissions_minus]
        )
        random.shuffle(values_emissions)
        values = values_emissions[:M]
        data[positions] = values

        return (data, {"Позиция": positions, "Значения": data[positions]})

    def harm(self, N: int, A0: int, f0: int, delta_t: float) -> np.ndarray:
        if delta_t > 1 / (2 * f0):
            return None

        k = np.arange(0, N)
        harm_data = A0 * np.sin(2 * np.pi * f0 * k * delta_t)

        return harm_data

    def polyharm(self, N: int, a_f_data: list, delta_t: float) -> np.ndarray:
        max_fi = max(params["f"] for params in a_f_data)
        if delta_t > 1 / (2 * max_fi):
            return None

        k = np.arange(0, N)
        values = np.zeros(N)
        for params in a_f_data:
            values += params["A"] * np.sin(2 * np.pi * params["f"] * k * delta_t)

        return values

    def add_model(self, data1: np.ndarray, data2: np.ndarray) -> np.ndarray:
        min_len = min(len(data1), len(data2))
        values1 = data1[:min_len]
        values2 = data2[:min_len]
        return values1 + values2

    def multi_model(self, data1: np.ndarray, data2: np.ndarray) -> np.ndarray:
        min_len = min(len(data1), len(data2))
        values1 = data1[:min_len]
        values2 = data2[:min_len]
        return values1 * values2
