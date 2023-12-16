import os
import sys
import wave

import numpy as np
import streamlit as st
import plotly.express as px
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

add_page_title()
show_pages_from_config()


class IN_OUT:
    @staticmethod
    def readWAV(file_path):
        with wave.open(file_path, "rb") as wf:
            rate = wf.getframerate()
            N = wf.getnframes()
            data = np.frombuffer(wf.readframes(N), dtype=np.int16)
        return data, rate, N

    @staticmethod
    def writeWAV(file_path, data, rate, volume_increase, increase_volume):
        if increase_volume:
            data = data * 10 ** (volume_increase / 20.0)
            data = np.clip(data, -32768, 32767).astype(np.int16)

        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(rate)

            if increase_volume:
                wf.writeframes(data.tobytes())
            else:
                wf.writeframes(data[: int(rate * 3)].tobytes())

        if increase_volume:
            st.audio(data, format="audio/wav", sample_rate=rate)

        return data, rate


def main():
    st.sidebar.title("Опции Обработки Аудио")
    selected_option = st.sidebar.radio("Выберите опцию", ["Чтение WAV", "Запись WAV"])

    if selected_option == "Чтение WAV":
        st.subheader("Чтение WAV Файла")

        uploaded_file = st.file_uploader("Выберите WAV файл", type=["wav"])
        if uploaded_file is not None:
            audio_data, sample_rate, duration = IN_OUT.readWAV(uploaded_file)

            st.write(f"Частота дискретизации: {sample_rate} Гц")
            st.write(f"Длительность записи: {duration / sample_rate:.2f} секунд")

            short_fragment = audio_data[: int(sample_rate * 3)]
            st.audio(short_fragment, format="audio/wav", sample_rate=sample_rate)

            fig = px.line(
                x=np.arange(len(short_fragment)) / sample_rate,
                y=short_fragment,
                labels={"x": "Время (сек)", "y": "Амплитуда"},
            )
            fig.update_traces(line=dict(color="green", width=2))
            fig.update_layout(
                xaxis_title="Время (сек)",
                yaxis_title="Амплитуда",
                hovermode="x",
            )
            st.plotly_chart(fig, use_container_width=True)

    elif selected_option == "Запись WAV":
        st.subheader("Запись WAV Файла")

        uploaded_file = st.file_uploader("Выберите WAV файл для записи", type=["wav"])
        if uploaded_file is not None:
            audio_data, sample_rate, duration = IN_OUT.readWAV(uploaded_file)

            volume_increase = st.slider(
                "Увеличение Громкости (dB)", min_value=-20, max_value=20, value=10
            )
            increase_volume = st.checkbox("Увеличить Громкость", key="increase_volume")

            if st.button("Записать Усиленный WAV"):
                IN_OUT.writeWAV(
                    "amplified_audio.wav",
                    audio_data,
                    sample_rate,
                    volume_increase,
                    increase_volume,
                )
                st.success("WAV файл с увеличенной громкостью успешно записан.")


if __name__ == "__main__":
    main()
