import os
import sys
import wave

import numpy as np
import soundfile as sf
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from model import utils as model_utils

add_page_title()
show_pages_from_config()


class IN_OUT:
    def __init__(self):
        self.rate = None
        self.frames = None
        self.data = None

    def readWAV(self, wav_file):
        with wave.open(wav_file, "rb") as wave_file:
            self.rate = wave_file.getframerate()
            self.frames = wave_file.getnframes()
            self.data = np.frombuffer(wave_file.readframes(self.frames), dtype=np.int16)

    def writeWAV(self, output_path, data):
        sf.write(output_path, data, self.rate)


def display_audio_signal(data, rate, duration=3, label=""):
    st.markdown(
        f"<h3 style='text-align: center;'>Аудио сигнал {label}</h3>",
        unsafe_allow_html=True,
    )
    st.audio(data, sample_rate=rate, format="audio/wav")
    st.markdown(f"{label} (первые {duration} секунд)")
    st.audio(data[: rate * duration], sample_rate=rate, format="audio/wav")


def main():
    in_out = IN_OUT()

    st.markdown(
        f"<h1 style='text-align: center;'>Запись и чтение wav-файлов</h1>",
        unsafe_allow_html=True,
    )

    wav_file = st.file_uploader("Загрузите wav-файл", type=["wav"])

    if wav_file is not None:
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
        # st.markdown(
        #     f"<p style='text-align: center;'>Количество отсчетов: {in_out.frames / in_out.rate:.2f} сек</p>",
        #     unsafe_allow_html=True,
        # )

        st.subheader("График сигнала")
        model_utils.plot_line_chart(
            param1=np.arange(len(in_out.data)) / in_out.rate,
            param2=in_out.data,
            x_label="Время",
            y_label="Значение сигнала",
            color="limegreen",
            width=2,
        )

        display_audio_signal(in_out.data, in_out.rate)

        increased_volume_data = (in_out.data * 1.5).astype(np.int32)

        st.subheader("График сигнала после изменения громкости")
        model_utils.plot_line_chart(
            param1=np.arange(len(increased_volume_data)) / in_out.rate,
            param2=increased_volume_data,
            x_label="Время",
            y_label="Значение сигнала",
            color="limegreen",
            width=2,
        )

        display_audio_signal(
            increased_volume_data, in_out.rate, label="после изменения громкости"
        )
        in_out.writeWAV("data/wav/" + "audio" + ".wav", increased_volume_data)


if __name__ == "__main__":
    main()
