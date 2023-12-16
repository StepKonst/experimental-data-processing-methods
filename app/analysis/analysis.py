__all__ = ["Analysis"]

import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew


class Analysis:
    def statistics(self, data: np.ndarray) -> dict:
        return {
            "Минимальное значение": np.min(data),
            "Максимальное значение": np.max(data),
            "Среднее значение": np.mean(data),
            "Дисперсия": np.var(data),
            "Стандартное отклонение": np.std(data),
            "Ассиметрия": skew(data),
            "Коэффициент ассиметрии": skew(data) / np.std(data),
            "Эксцесс": kurtosis(data, fisher=False),
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

    def hist(self, data: np.ndarray, M: int) -> pd.DataFrame:
        hist, bins = np.histogram(data, M, density=True)
        bin_center = (bins[:-1] + bins[1:]) / 2

        return pd.DataFrame({"x": bin_center, "y": hist})

    def acf(self, data: np.ndarray, function_type: str) -> pd.DataFrame:
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

    def ccf(self, datax: np.ndarray, datay: np.ndarray) -> pd.DataFrame:
        if len(datax) != len(datay):
            raise ValueError("Длины входных данных не совпадают")

        n = len(datax)
        l_values = np.arange(0, n)
        x_mean = np.mean(datax)
        y_mean = np.mean(datay)
        ccf_values = (
            np.correlate(datax - x_mean, datay - y_mean, mode="full")[:n][::-1] / n
        )

        return pd.DataFrame({"L": l_values, "CCF": ccf_values})

    def fourier(self, data: np.ndarray) -> pd.DataFrame:
        fourier_transform = np.fft.fft(data)
        amplitude_spectrum = np.abs(fourier_transform)

        return pd.DataFrame(
            {
                "Re[Xn]": fourier_transform.real,
                "Im[Xn]": fourier_transform.imag,
                "|Xn|": amplitude_spectrum,
            }
        )

    def fourier_proc(self, data):
        N = len(data)
        freqs = np.arange(N)
        cos_vals = np.cos(2 * np.pi * np.outer(freqs, freqs) / N)
        sin_vals = np.sin(2 * np.pi * np.outer(freqs, freqs) / N)
        Re_Xn = np.dot(data, cos_vals)
        Im_Xn = np.dot(data, sin_vals)
        Re_Xn /= N
        Im_Xn /= N
        Xn = np.sqrt((Re_Xn**2) + (Im_Xn**2))
        return Xn.tolist()

    def spectr_fourier(self, data: np.ndarray, dt: float) -> pd.DataFrame:
        n = len(data) // 2
        fourier_data = self.fourier(data)
        xn_values = fourier_data["|Xn|"].values
        f_border = 1 / (2 * dt)
        delta_f = f_border / n
        frequencies = np.arange(n) * delta_f

        return pd.DataFrame({"f": frequencies, "|Xn|": xn_values[:n]})

    def spectrFourier(self, X_n, N, dt):
        out_data = []
        f_border = 1 / (2 * dt)
        df = 2 * f_border / N
        for i in range(N):
            out_data.append(X_n[i] * df)
        return out_data

    def spectr_fourier_window(
        self, data: np.ndarray, dt: float, L: int
    ) -> pd.DataFrame:
        n = len(data)
        window = np.concatenate([np.ones(n - L), np.zeros(L)])
        data_windowed = data * window
        fourier_data = self.fourier(data_windowed)
        xn_values = fourier_data["|Xn|"].values
        n = len(data) // 2
        f_border = 1 / (2 * dt)
        delta_f = f_border / n
        frequencies = np.arange(n) * delta_f

        return pd.DataFrame({"f": frequencies, "|Xn|": xn_values[:n]})

    def frequencyResponse(self, data, N):
        out_data = []
        furier = self.fourier_proc(data)
        for i in range(N):
            out_data.append(furier[i] * N)
        return out_data

    def convolution(self, x, h, N, M):
        out_data = []
        for i in range(N):
            y = 0
            for j in range(M):
                y += x[i - j] * h[j]
            out_data.append(y)
        return out_data
