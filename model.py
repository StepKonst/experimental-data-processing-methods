import numpy as np


class Model:
    def trend(self, type, a, b, N):
        t = np.arange(0, N)

        trend_dict = {
            "Linear Up": a * t + b,
            "Linear Down": -a * t + b,
            "Nonlinear Up": b * np.exp(a * t),
            "Nonlinear Down": b * np.exp(-a * t),
        }

        x = trend_dict.get(type)
        return t, x
