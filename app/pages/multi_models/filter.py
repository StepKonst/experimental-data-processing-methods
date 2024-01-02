import os
import sys

import numpy as np
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from analysis import Analysis
from model import Model
from model import utils as model_utils
from processing import Processing

model = Model()
analysis = Analysis()
processing = Processing()

file_path = "files/pgp_dt0005.dat"

add_page_title()
show_pages_from_config()


def main():
    st.sidebar.title("Настройки")

    fc_value = st.sidebar.number_input(
        "Выберите значение fc", min_value=1, max_value=100, step=1, value=50
    )
    dt_value = st.sidebar.number_input(
        "Выберите значение dt", min_value=0.0001, max_value=1.0, step=0.001, value=0.002
    )
    m_value = st.sidebar.number_input(
        "Выберите значение m", min_value=1, max_value=500, step=1, value=64
    )
    fc1_value = st.sidebar.number_input(
        "Выберите значение fc1", min_value=1, max_value=100, step=1, value=35
    )
    fc2_value = st.sidebar.number_input(
        "Выберите значение fc2", min_value=1, max_value=100, step=1, value=75
    )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")

    with open(file_path, "rb") as file:
        binary_data = file.read()

    file_data = np.frombuffer(binary_data, dtype=np.float32)

    file_data_furier = analysis.fourier_proc(file_data)
    file_data_X_n = analysis.spectrFourier(
        [i for i in range(len(file_data))], len(file_data), dt_value
    )

    # Фильтры
    lpw = processing.lpf(fc_value, m_value, dt_value)
    ref_lpw = processing.reflect_lpf(lpw)
    hpf = processing.hpf(fc_value, m_value, dt_value)
    bpf = processing.bpf(fc1_value, fc2_value, m_value, dt_value)
    bsf = processing.bsf(fc1_value, fc2_value, m_value, dt_value)

    # Частотные характеристики
    tf_ref_lpw = analysis.frequencyResponse(ref_lpw, 2 * m_value + 1)
    tf_hpf = analysis.frequencyResponse(hpf, 2 * m_value + 1)
    tf_bpf = analysis.frequencyResponse(bpf, 2 * m_value + 1)
    tf_bsf = analysis.frequencyResponse(bsf, 2 * m_value + 1)
    new_X_n = analysis.spectrFourier(
        [i for i in range(2 * m_value + 1)], 2 * m_value + 1, dt_value
    )

    # Свертки
    convolution_lpf = model.convol_model(
        file_data, ref_lpw, len(file_data), 2 * m_value + 1
    )
    convolution_hpf = model.convol_model(
        file_data, hpf, len(file_data), 2 * m_value + 1
    )
    convolution_bpf = model.convol_model(
        file_data, bpf, len(file_data), 2 * m_value + 1
    )
    convolution_bsf = model.convol_model(
        file_data, bsf, len(file_data), 2 * m_value + 1
    )

    convolution_lpf_furier = analysis.fourier_proc(convolution_lpf)
    convolution_hpf_furier = analysis.fourier_proc(convolution_hpf)
    convolution_bpf_furier = analysis.fourier_proc(convolution_bpf)
    convolution_bsf_furier = analysis.fourier_proc(convolution_bsf)

    st.subheader("График входного сигнала файла pgp_dt0005.dat")
    model_utils.plot_line_chart(
        param1=range(len(file_data)),
        param2=file_data,
        x_label="Время",
        y_label="Значение сигнала",
        color="limegreen",
        width=1,
    )

    st.subheader("График спектра сигнала")
    model_utils.plot_line_chart(
        param1=file_data_X_n[: len(file_data_X_n) // 2],
        param2=file_data_furier[: len(file_data_furier) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="limegreen",
        width=2,
    )

    st.title("Фильтр низких частот")
    st.subheader("График частотной характеристики LPF")
    model_utils.plot_line_chart(
        param1=new_X_n[: len(new_X_n) // 2],
        param2=tf_ref_lpw[: len(tf_ref_lpw) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="coral",
        width=2,
    )

    st.subheader("График свертки сигнала и функции LPF")
    model_utils.plot_line_chart(
        param1=range(len(convolution_lpf)),
        param2=convolution_lpf,
        x_label="Время",
        y_label="Значение сигнала",
        color="coral",
        width=1,
    )

    st.subheader("График спектра свертки")
    model_utils.plot_line_chart(
        param1=file_data_X_n[: len(file_data_X_n) // 2],
        param2=convolution_lpf_furier[: len(convolution_lpf_furier) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="coral",
        width=2,
    )

    st.divider()
    st.title("Фильтр высоких частот")
    st.subheader("График частотной характеристики HPF")
    model_utils.plot_line_chart(
        param1=new_X_n[: len(new_X_n) // 2],
        param2=tf_hpf[: len(tf_hpf) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="fuchsia",
        width=2,
    )

    st.subheader("График свертки сигнала и функции HPF")
    model_utils.plot_line_chart(
        param1=range(len(convolution_hpf)),
        param2=convolution_hpf,
        x_label="Время",
        y_label="Значение сигнала",
        color="fuchsia",
        width=1,
    )

    st.subheader("График спектра свертки")
    model_utils.plot_line_chart(
        param1=file_data_X_n[: len(file_data_X_n) // 2],
        param2=convolution_hpf_furier[: len(convolution_hpf_furier) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="fuchsia",
        width=2,
    )

    st.divider()
    st.title("Полосовой фильтр")
    st.subheader("График частотной характеристики BPF")
    model_utils.plot_line_chart(
        param1=new_X_n[: len(new_X_n) // 2],
        param2=tf_bpf[: len(tf_bpf) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="deepskyblue",
        width=2,
    )

    st.subheader("График свертки сигнала и функции BPF")
    model_utils.plot_line_chart(
        param1=range(len(convolution_bpf)),
        param2=convolution_bpf,
        x_label="Время",
        y_label="Значение сигнала",
        color="deepskyblue",
        width=1,
    )

    st.subheader("График спектра свертки")
    model_utils.plot_line_chart(
        param1=file_data_X_n[: len(file_data_X_n) // 2],
        param2=convolution_bpf_furier[: len(convolution_bpf_furier) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="deepskyblue",
        width=2,
    )

    st.divider()
    st.title("Режекторный фильтр")
    st.subheader("График частотной характеристики BSF")
    model_utils.plot_line_chart(
        param1=new_X_n[: len(new_X_n) // 2],
        param2=tf_bsf[: len(tf_bsf) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="indianred",
        width=2,
    )

    st.subheader("График свертки сигнала и функции BSF")
    model_utils.plot_line_chart(
        param1=range(len(convolution_bsf)),
        param2=convolution_bsf,
        x_label="Время",
        y_label="Значение сигнала",
        color="indianred",
        width=1,
    )

    st.subheader("График спектра свертки")
    model_utils.plot_line_chart(
        param1=file_data_X_n[: len(file_data_X_n) // 2],
        param2=convolution_bsf_furier[: len(convolution_bsf_furier) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="indianred",
        width=2,
    )


if __name__ == "__main__":
    main()
