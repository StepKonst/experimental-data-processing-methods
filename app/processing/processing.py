__all__ = ["Processing"]


import model
import numpy as np

model = model.Model()


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

    def antiNoise(self, data, N, M):
        return [np.mean([data[m][1][i] for m in range(M)]) for i in range(N)]

    def lpf(self, fc, m, dt):
        d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
        fact = 2 * fc * dt
        lpw = [fact] + [0] * m
        arg = fact * np.pi
        for i in range(1, m + 1):
            lpw[i] = np.sin(arg * i) / (np.pi * i)
        lpw[m] /= 2.0
        sumg = lpw[0]
        for i in range(1, m + 1):
            sum = d[0]
            arg = np.pi * i / m
            for k in range(1, 4):
                sum += 2.0 * d[k] * np.cos(arg * k)
            lpw[i] *= sum
            sumg += 2 * lpw[i]
        for i in range(m + 1):
            lpw[i] /= sumg
        return lpw

    def reflect_lpf(self, lpw):
        reflection = []
        for i in range(len(lpw) - 1, 0, -1):
            reflection.append(lpw[i])
        reflection.extend(lpw)
        return reflection

    def hpf(self, fc, m, dt):
        lpw = self.reflect_lpf(self.lpf(fc, m, dt))
        hpw = [-lpw[k] if k != m else 1 - lpw[k] for k in range(2 * m + 1)]
        return hpw

    def bpf(self, fc1, fc2, m, dt):
        lpw1 = self.reflect_lpf(self.lpf(fc1, m, dt))
        lpw2 = self.reflect_lpf(self.lpf(fc2, m, dt))
        bpw = [lpw2[k] - lpw1[k] for k in range(2 * m + 1)]
        return bpw

    def bsf(self, fc1, fc2, m, dt):
        lpw1 = self.reflect_lpf(self.lpf(fc1, m, dt))
        lpw2 = self.reflect_lpf(self.lpf(fc2, m, dt))
        bsw = [
            1.0 + lpw1[k] - lpw2[k] if k == m else lpw1[k] - lpw2[k]
            for k in range(2 * m + 1)
        ]
        return bsw
