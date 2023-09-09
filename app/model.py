import numpy as np


class Model:
    def trend(self, type, a, b, N):
        time_values = np.arange(0, N)

        trend_dict = {
            "Линейно восходящий тренд": a * time_values + b,
            "Линейно нисходящий тренд": -a * time_values + b,
            "Нелинейно восходящий тренд": b * np.exp(a * time_values),
            "Нелинейно нисходящий тренд": b * np.exp(-a * time_values),
        }

        trend_values = trend_dict.get(type)
        return time_values, trend_values

    def combined_trend(self, type1, a1, b1, type2, a2, b2, N):
        time_values1, trend_values1 = self.trend(type1, a1, b1, N // 2)
        time_values2, trend_values2 = self.trend(type2, a2, b2, N // 2)

        combined_time_values = time_values1 + time_values2
        combined_trend_values = trend_values1 + trend_values2

        return combined_time_values, combined_trend_values
