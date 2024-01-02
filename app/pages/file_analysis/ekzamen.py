import os
import sys

import numpy as np
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import analysis
import model
import processing
from analysis import utils as analysis_utils
from model import utils as model_utils

model = model.Model()
analysis = analysis.Analysis()
processing = processing.Processing()

add_page_title()
show_pages_from_config()


def main():
    file_path = "files/v36.bin"
    data = np.fromfile(file_path, dtype=np.float32)

    st.subheader("График входного сигнала")
    model_utils.plot_line_chart(
        param1=range(len(data)),
        param2=data,
        x_label="Время",
        y_label="Значение сигнала",
        color="dodgerblue",
        width=2,
    )

    st.subheader("Пробуем удалить выбросы с помощью функции analysis.antispike()")
    st.markdown(
        """Для подавления неправдоподобных значений 𝑥𝑘, 
        выходящих за пределы диапазона R 
        используется простейший 3-хточечный фильтр линейной интерполяции"""
    )
    range_noise = st.number_input(
        "Введите значение диапозона для модели шума", value=10
    )
    anti_spike_noise = processing.antispike(data, range_noise)
    model_utils.plot_line_chart(
        range(len(anti_spike_noise)),
        anti_spike_noise,
        "Время",
        "Значение аддитивной модели",
        "dodgerblue",
        width=2,
    )

    st.subheader("Проверим, линейный ли тут тренд...")
    st.markdown(
        """Для этого используем функцию antisihift(), для обнаружения и 
        удаления смещения в данных data путем нахождения среднего значения 
        (центра рассеивания) и вычитания его из всех значений данных."""
    )
    check_on_linear = processing.antishift(anti_spike_noise)
    model_utils.plot_line_chart(
        range(len(check_on_linear)),
        check_on_linear,
        "Время",
        "Значение",
        "dodgerblue",
        width=2,
    )

    st.subheader(
        "Нужно попробовать удалить тренд. Для этого применим processing.antitrendnonlinear()"
    )
    st.markdown(
        "Удаление линейного тренда осуществляем путем вычисления первой производной данных data"
    )
    process = processing.antitrendnonlinear(anti_spike_noise, W=10)[:980]
    model_utils.plot_line_chart(
        range(len(process)), process, "Время", "Значение", "dodgerblue", width=2
    )
    bpf = processing.bpf(fc1=219, fc2=221, m=128, dt=0.0005)

    spectr = analysis.spectr_fourier(process, dt=0.0005)
    st.subheader("График амплитудного спектра Фурье")
    analysis_utils.plot_fourier_spectrum(spectr, "Частота", "Амплитуда", "dodgerblue")

    data_filter = model.convol_model(process, bpf, len(process), 2 * 64 + 1)

    convolution_bsf_furier = analysis.fourier_proc(data_filter)
    st.subheader("График спектра Фурье после фильтрации")
    model_utils.plot_line_chart(
        param1=range(len(convolution_bsf_furier) // 2),
        param2=convolution_bsf_furier[: len(convolution_bsf_furier) // 2],
        x_label="Частота",
        y_label="Амплитуда",
        color="dodgerblue",
        width=1,
    )

    st.subheader("График после применения полосового фильтра")
    model_utils.plot_line_chart(
        param1=np.arange(len(data_filter)),
        param2=data_filter,
        x_label="Фреймы",
        y_label="Значение сигнала",
        color="dodgerblue",
        width=2,
    )

    statistical_characteristics = analysis.statistics(np.array(data_filter))
    model_utils.get_dataframe(statistical_characteristics)


if __name__ == "__main__":
    main()
