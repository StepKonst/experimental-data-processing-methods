import os
import sys
import wave

import numpy as np
import soundfile as sf
import streamlit as st
from soundlit import AudioWidget
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from model import Model
from model import utils as model_utils

model = Model()
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

    def writeWAV(self, output_path, data, rate=None):
        sf.write(output_path, data, rate)


def display_audio_signal(data, rate, duration=3, label=""):
    st.markdown(
        f"<h3 style='text-align: center;'>Аудио сигнал {label}</h3>",
        unsafe_allow_html=True,
    )
    st.audio(data, sample_rate=rate, format="audio/wav")
    st.markdown(f"{label} (первые {duration} секунд)")
    st.audio(data[: rate * duration], sample_rate=rate, format="audio/wav")


def rw(c1, c2, n1, n2, n3, n4, N):
    pw = [1 for _ in range(n1)]
    pw.extend([c1 for _ in range(n1, n2 + 1)])
    pw.extend([1 for _ in range(n2 + 1, n3)])
    pw.extend([c2 for _ in range(n3, n4 + 1)])
    pw.extend([1 for _ in range(n4 + 1, N)])
    return pw


def to_int16(data):
    new_data = []
    for i in range(len(data)):
        new_data.append(np.int16(data[i]))
    return new_data


def main():
    sample_rate = 22050
    in_out = IN_OUT()
    widget = AudioWidget(sample_rate=sample_rate, max_duration=3, mono=True)
    audio_data = widget.record_audio()
    # in_out.writeWAV("data/wav/demo/original/test.wav", audio_data[0], rate=sample_rate)

    if audio_data:
        st.success(f"Аудио успешно записано.")
        frame = len(audio_data[0])
        audio_data = audio_data[0]
        st.markdown(
            "<h3 style='text-align: center;'>Информация о файле</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center;'>Частота дискретизации: {sample_rate} Гц</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center;'>Количество отсчетов: {frame}</p>",
            unsafe_allow_html=True,
        )

        st.subheader("График сигнала")
        model_utils.plot_line_chart(
            param1=np.arange(frame),
            param2=audio_data,
            x_label="Время",
            y_label="Значение сигнала",
            color="limegreen",
            width=2,
        )

        x1 = 15000
        x2 = 25000
        x3 = 28000
        x4 = 36300

        stressed_max = max(audio_data[x1:x2])
        unstressed_max = max(audio_data[x3:x4])
        c1 = unstressed_max / stressed_max
        c2 = stressed_max / unstressed_max

        r_w = rw(c1, c2, x1, x2, x3, x4, frame)
        new_sound = model.multi_model(audio_data, r_w)
        st.audio(new_sound, sample_rate=sample_rate, format="audio/wav")
        in_out.writeWAV("data/wav/new.wav", new_sound, rate=sample_rate)
        st.success(f"Аудиофайл new.wav успешно записан.")

    else:
        st.warning("Не удалось записать аудио. Пожалуйста, повторите попытку.")

    wav_file = st.file_uploader("Загрузите wav-файл", type=["wav"])

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

        st.subheader("Осциллограмма")
        model_utils.plot_line_chart(
            param1=np.arange(len(in_out.data)),
            param2=in_out.data,
            x_label="Время",
            y_label="Значение сигнала",
            color="limegreen",
            width=2,
        )

        # # ДАЧА
        # x1 = 17900
        # x2 = 27800
        # x3 = 32000
        # x4 = 38800

        # ЛЕТО
        x1 = 13900
        x2 = 24000
        x3 = 31000
        x4 = 35300

        stressed_max = max(in_out.data[x1:x2])
        unstressed_max = max(in_out.data[x3:x4])
        c1 = unstressed_max / stressed_max
        c2 = stressed_max / unstressed_max

        r_w = rw(c1, c2, x1, x2, x3, x4, in_out.frames)
        new_sound = model.multi_model(in_out.data, r_w)

        display_audio_signal(new_sound, in_out.rate)

        new_sound = to_int16(new_sound)
        in_out.writeWAV(
            "data/wav/demo/processed/dacha.wav", new_sound, rate=in_out.rate
        )


if __name__ == "__main__":
    main()
