import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from model import Model
from model import utils as model_utils

model = Model()

add_page_title()
show_pages_from_config()


def main():
    st.sidebar.title("Настройки")

    n_value = st.sidebar.number_input(
        'Выберите общее значение "N"', min_value=1, max_value=10000, step=1, value=1000
    )
    dt_value = st.sidebar.number_input(
        'Выберите общее значение "delta_t"',
        min_value=0.0,
        max_value=0.1,
        step=0.001,
        value=0.005,
    )

    st.sidebar.subheader("Настройки экспоненциального тренда")
    a_trend, b_trend = model_utils.get_exponential_trend_data()
    exponential_trend_data = model.descending_exponential_trend(
        n=n_value, a=a_trend, b=b_trend, dt=dt_value
    )

    st.sidebar.subheader("Настройки гармоничного процесса")
    a_harm = st.sidebar.number_input(
        "Выберите значение амплитуды",
        min_value=1,
        max_value=1000,
        step=1,
        value=1,
    )
    f_harm = st.sidebar.number_input(
        "Выберите значение частоты",
        min_value=0.1,
        max_value=600.0,
        step=100.0,
        value=7.0,
    )

    harm_data = model.harm(n_value, a_harm, f_harm, dt_value)
    if harm_data is None:
        st.error(
            "Некоректное значение временного интервала для гармонического процесса"
        )
        sys.exit()

    multimodel_noise_harm = model.multi_model(exponential_trend_data, harm_data)
    heart_impulse = [
        multimodel_noise_harm[i] * 120 / max(multimodel_noise_harm)
        for i in range(len(multimodel_noise_harm))
    ]
    rhythm = model.rhythm(N=n_value, M=200, R=1, Rs=0.1)
    convolution = model.convolModel(rhythm, heart_impulse, M=200)

    st.subheader("Управляющая функция ритма")
    model_utils.plot_line_chart(rhythm, "Время", "Амплитуда", "blue")

    st.subheader("Импульсная реакция модели сердечной мышцы")
    model_utils.plot_line_chart(heart_impulse, "Время", "Амплитуда", "orange")

    st.subheader("Результат свертки")
    model_utils.plot_line_chart(convolution, "Время", "Амплитуда", "green")

    st.title("Патологическая кардиограмма")
    noise_data = model.noise(n_value, 0.001)[1]
    emission_data, _ = model.spikes(N=n_value, M=5, R=2, Rs=1)
    additive_noise_emission = model.add_model(emission_data, noise_data)

    rhythm = [abs(spike) for spike in additive_noise_emission]
    convolution = model.convolModel(rhythm, heart_impulse, M=200)

    st.subheader("Управляющая функция ритма")
    model_utils.plot_line_chart(rhythm, "Время", "Амплитуда", "blue")

    st.subheader("Результат свертки")
    model_utils.plot_line_chart(convolution, "Время", "Амплитуда", "green")

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
