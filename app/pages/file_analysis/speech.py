import os
import sys
import wave

import numpy as np
import soundfile as sf
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from model import Model
from analysis import Analysis
from processing import Processing
from model import utils as model_utils
from analysis import utils as analysis_utils

model = Model()
analysis = Analysis()
processing = Processing()
add_page_title()
show_pages_from_config()


class IN_OUT:
    def __init__(self):
        self.rate = None
        self.frames = None
        self.data = None

    def readWAV(self, wav_file):
        self.data, self.rate = sf.read(wav_file)

        if len(self.data.shape) > 1:
            self.data = self.data[:, 0]

        time_array = np.arange(len(self.data)) / self.rate
        self.frames = len(time_array)
        # with wave.open(wav_file, "rb") as wave_file:
        #     self.rate = wave_file.getframerate()
        #     self.frames = wave_file.getnframes()
        #     self.data = np.frombuffer(wave_file.readframes(self.frames), dtype=np.int16)

    def writeWAV(self, output_path, data):
        sf.write(output_path, data, self.rate)


def main():
    in_out = IN_OUT()
    wav_file = st.file_uploader("Загрузите оригинальный wav-файл", type=["wav"])
    wav_file_proc = st.file_uploader("Загрузите wav-файл после обработки", type=["wav"])

    if wav_file:
        in_out.readWAV(wav_file)

        st.markdown(
            "<h3 style='text-align: center;'>Информация о файле</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center;'>Частота дискретизации: {in_out.rate} Гц</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center;'>Количество отсчетов: {in_out.frames}</p>",
            unsafe_allow_html=True,
        )

        st.subheader("График сигнала")
        model_utils.plot_line_chart(
            param1=np.arange(len(in_out.data)),
            param2=in_out.data,
            x_label="Фреймы",
            y_label="Значение сигнала",
            color="fuchsia",
            width=2,
        )

        st.subheader("График амплитудного спектра Фурье всего сигнала")
        signal_spectr = analysis.spectr_fourier(in_out.data, dt=1 / in_out.rate)
        analysis_utils.plot_fourier_spectrum(
            signal_spectr, "Частота", "Амплитуда", "fuchsia"
        )
        st.divider()

        # ДАЧА
        x1 = 17900
        x2 = 27800
        x3 = 32000
        x4 = 38800

        st.subheader("График сигнала для первого слога")
        model_utils.plot_line_chart(
            param1=np.arange(len(in_out.data[x1:x2])),
            param2=in_out.data[x1:x2],
            x_label="Фреймы",
            y_label="Значение сигнала",
            color="deepskyblue",
            width=2,
        )
        st.subheader("График амплитудного спектра Фурье первого слога")
        first_syllable_spectr = analysis.spectr_fourier(
            in_out.data[x1:x2], dt=1 / in_out.rate
        )
        analysis_utils.plot_fourier_spectrum(
            first_syllable_spectr, "Частота", "Амплитуда", "deepskyblue"
        )

        st.divider()
        st.subheader("График сигнала для второго слога")
        model_utils.plot_line_chart(
            param1=np.arange(len(in_out.data[x3:x4])),
            param2=in_out.data[x3:x4],
            x_label="Фреймы",
            y_label="Значение сигнала",
            color="limegreen",
            width=2,
        )
        st.subheader("График амплитудного спектра Фурье второго слога")
        second_syllable_spectr = analysis.spectr_fourier(
            in_out.data[x3:x4], dt=1 / in_out.rate
        )
        analysis_utils.plot_fourier_spectrum(
            second_syllable_spectr, "Частота", "Амплитуда", "limegreen"
        )

    elif wav_file_proc:
        in_out.readWAV(wav_file_proc)

        st.markdown(
            "<h3 style='text-align: center;'>Информация о файле</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center;'>Частота дискретизации: {in_out.rate} Гц</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center;'>Количество отсчетов: {in_out.frames}</p>",
            unsafe_allow_html=True,
        )

        st.audio(in_out.data, sample_rate=in_out.rate, format="audio/wav")

        st.subheader("График сигнала")
        model_utils.plot_line_chart(
            param1=np.arange(len(in_out.data)),
            param2=in_out.data,
            x_label="Фреймы",
            y_label="Значение сигнала",
            color="fuchsia",
            width=2,
        )

        st.subheader("График амплитудного спектра Фурье всего сигнала")
        signal_spectr = analysis.spectr_fourier(in_out.data, dt=1 / in_out.rate)
        # signal_spectr["|Xn|"] = signal_spectr["|Xn|"].apply(lambda x: x / 100000)
        analysis_utils.plot_fourier_spectrum(
            signal_spectr, "Частота", "Амплитуда", "fuchsia"
        )
        st.divider()

        # ЛЕТО
        x1 = 13800
        x2 = 24300
        x3 = 30800
        x4 = 35800
        m = 128

        syl = st.radio("Выберите слог для анализа", ["Первый", "Второй"], key="syl")
        if syl == "Первый":
            st.subheader("График сигнала для первого слога")
            model_utils.plot_line_chart(
                param1=np.arange(len(in_out.data[x1:x2])),
                param2=in_out.data[x1:x2],
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="deepskyblue",
                width=2,
            )

            ote = 142
            f1e = 407
            f2e = 1680
            f3e = 2415
            f4e = 3082

            lpw = processing.lpf(ote, m, dt=1 / in_out.rate)
            low_pass_filter = processing.reflect_lpf(lpw)  # Основной тон

            band_pass_filter_F1 = processing.bpf(
                f1e - 50, f1e + 50, m, dt=1 / in_out.rate
            )
            band_pass_filter_F2 = processing.bpf(
                f2e - 50, f2e + 50, m, dt=1 / in_out.rate
            )
            band_pass_filter_F3 = processing.bpf(
                f3e - 50, f3e + 50, m, dt=1 / in_out.rate
            )
            high_pass_filter_F4 = processing.hpf(f4e - 50, m, dt=1 / in_out.rate)

            # Convolution
            patch = model.convol_model(
                in_out.data[x1:x2], low_pass_filter, len(in_out.data[x1:x2]), 2 * m + 1
            )
            formant_1 = model.convol_model(
                in_out.data[x1:x2],
                band_pass_filter_F1,
                len(in_out.data[x1:x2]),
                2 * m + 1,
            )
            formant_2 = model.convol_model(
                in_out.data[x1:x2],
                band_pass_filter_F2,
                len(in_out.data[x1:x2]),
                2 * m + 1,
            )
            formant_3 = model.convol_model(
                in_out.data[x1:x2],
                band_pass_filter_F3,
                len(in_out.data[x1:x2]),
                2 * m + 1,
            )
            formant_4 = model.convol_model(
                in_out.data[x1:x2],
                high_pass_filter_F4,
                len(in_out.data[x1:x2]),
                2 * m + 1,
            )

            st.subheader("График амплитудного спектра Фурье первого слога")
            first_syllable_spectr = analysis.spectr_fourier(
                in_out.data[x1:x2], dt=1 / in_out.rate
            )
            # first_syllable_spectr["|Xn|"] = first_syllable_spectr["|Xn|"].apply(
            #     lambda x: x / 100000
            # )
            analysis_utils.plot_fourier_spectrum(
                first_syllable_spectr[: len(first_syllable_spectr) // 2],
                "Частота",
                "Амплитуда",
                "deepskyblue",
            )

            st.subheader("График основного тона")
            model_utils.plot_line_chart(
                param1=np.arange(len(patch)),
                param2=patch,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="deepskyblue",
                width=2,
            )
            st.audio(np.array(patch), format="audio/wav", sample_rate=in_out.rate)

            st.subheader("График первой форманты")
            model_utils.plot_line_chart(
                param1=np.arange(len(formant_1)),
                param2=formant_1,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="deepskyblue",
                width=2,
            )
            st.audio(np.array(formant_1), sample_rate=in_out.rate, format="audio/wav")

            st.subheader("График второй форманты")
            model_utils.plot_line_chart(
                param1=np.arange(len(formant_2)),
                param2=formant_2,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="deepskyblue",
                width=2,
            )
            st.audio(np.array(formant_2), sample_rate=in_out.rate, format="audio/wav")

            st.subheader("График третьей форманты")
            model_utils.plot_line_chart(
                param1=np.arange(len(formant_3)),
                param2=formant_3,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="deepskyblue",
                width=2,
            )
            st.audio(np.array(formant_3), sample_rate=in_out.rate, format="audio/wav")

            st.subheader("График четвертой форманты")
            model_utils.plot_line_chart(
                param1=np.arange(len(formant_4)),
                param2=formant_4,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="deepskyblue",
                width=2,
            )
            st.audio(np.array(formant_4), sample_rate=in_out.rate, format="audio/wav")

        elif syl == "Второй":
            st.subheader("График сигнала для второго слога")
            model_utils.plot_line_chart(
                param1=np.arange(len(in_out.data[x3:x4])),
                param2=in_out.data[x3:x4],
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="limegreen",
                width=2,
            )
            st.subheader("График амплитудного спектра Фурье второго слога")
            second_syllable_spectr = analysis.spectr_fourier(
                in_out.data[x3:x4], dt=1 / in_out.rate
            )
            # second_syllable_spectr["|Xn|"] = second_syllable_spectr["|Xn|"].apply(
            #     lambda x: x / 100000
            # )
            analysis_utils.plot_fourier_spectrum(
                second_syllable_spectr, "Частота", "Амплитуда", "limegreen"
            )

            oto = 114
            f1o = 454
            f2o = 979
            f3o = 2372
            f40 = 3087

            lpw = processing.lpf(oto, m, dt=1 / in_out.rate)
            low_pass_filter = processing.reflect_lpf(lpw)  # Основной тон

            band_pass_filter_F1 = processing.bpf(
                f1o - 50, f1o + 50, m, dt=1 / in_out.rate
            )
            band_pass_filter_F2 = processing.bpf(
                f2o - 50, f2o + 50, m, dt=1 / in_out.rate
            )
            band_pass_filter_F3 = processing.bpf(
                f3o - 50, f3o + 50, m, dt=1 / in_out.rate
            )
            high_pass_filter_F4 = processing.hpf(f40 - 50, m, dt=1 / in_out.rate)

            # Convolution
            patch = model.convol_model(
                in_out.data[x3:x4], low_pass_filter, len(in_out.data[x3:x4]), 2 * m + 1
            )
            formant_1 = model.convol_model(
                in_out.data[x3:x4],
                band_pass_filter_F1,
                len(in_out.data[x3:x4]),
                2 * m + 1,
            )
            formant_2 = model.convol_model(
                in_out.data[x3:x4],
                band_pass_filter_F2,
                len(in_out.data[x3:x4]),
                2 * m + 1,
            )
            formant_3 = model.convol_model(
                in_out.data[x3:x4],
                band_pass_filter_F3,
                len(in_out.data[x3:x4]),
                2 * m + 1,
            )
            formant_4 = model.convol_model(
                in_out.data[x3:x4],
                high_pass_filter_F4,
                len(in_out.data[x3:x4]),
                2 * m + 1,
            )

            st.subheader("График основного тона")
            model_utils.plot_line_chart(
                param1=np.arange(len(patch)),
                param2=patch,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="limegreen",
                width=2,
            )
            st.audio(np.array(patch), format="audio/wav", sample_rate=in_out.rate)

            st.subheader("График первой форманты")
            model_utils.plot_line_chart(
                param1=np.arange(len(formant_1)),
                param2=formant_1,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="limegreen",
                width=2,
            )
            st.audio(np.array(formant_1), format="audio/wav", sample_rate=in_out.rate)

            st.subheader("График второй форманты")
            model_utils.plot_line_chart(
                param1=np.arange(len(formant_2)),
                param2=formant_2,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="limegreen",
                width=2,
            )
            st.audio(np.array(formant_2), format="audio/wav", sample_rate=in_out.rate)

            st.subheader("График третьей форманты")
            model_utils.plot_line_chart(
                param1=np.arange(len(formant_3)),
                param2=formant_3,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="limegreen",
                width=2,
            )
            st.audio(np.array(formant_3), format="audio/wav", sample_rate=in_out.rate)

            st.subheader("График четвертой форманты")
            model_utils.plot_line_chart(
                param1=np.arange(len(formant_4)),
                param2=formant_4,
                x_label="Фреймы",
                y_label="Значение сигнала",
                color="limegreen",
                width=2,
            )
            st.audio(np.array(formant_4), format="audio/wav", sample_rate=in_out.rate)


if __name__ == "__main__":
    main()
