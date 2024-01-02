import os
import sys

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
    st.sidebar.title("Настройки")
    n_value, r_value, c_value, segment = model_utils.get_noise_value()

    noise_data = model_utils.get_my_noise(n_value=n_value, r_value=r_value)
    noise_data_cross = model.noise(n_value, r_value)[1]

    data = model.shift(noise_data, c_value, segment[0], segment[1])
    data_cross = model.shift(noise_data_cross, c_value, segment[0], segment[1])

    st.sidebar.success(f"Выбранный отрезок: [{segment[0]}, {segment[1]}]")

    model_utils.plot_line_chart(
        range(len(data)), data, "Время", "Значение шума", "red", width=1
    )

    statistical_characteristics = analysis.statistics(data)
    model_utils.get_dataframe(statistical_characteristics)

    m = st.sidebar.number_input(
        "Выберите количество сегментов для шума с использованием несложного генератора случайных чисел:",
        step=1,
        value=5,
        max_value=50,
    )
    st.sidebar.success(analysis.stationarity(data, m))

    st.divider()
    st.markdown("#### Данные после удаления в них смещения")
    anti_shift_data = processing.antishift(data=data)
    model_utils.plot_line_chart(
        range(len(anti_shift_data)),
        anti_shift_data,
        "Время",
        "Значение шума",
        "red",
        width=1,
    )

    st.divider()
    analysis_utils.distribution_density(data, "red")

    st.divider()
    st.markdown("#### График Автокорреляционной функции")
    acf = analysis.acf(data, "Автокорреляционная функция")
    analysis_utils.plot_autocorrelation(
        acf.set_index("L"), "Время", "Значение автокорреляции", "red"
    )

    st.divider()
    st.markdown("#### График Ковариационной функции")
    cf = analysis.acf(data, "Ковариационная функция")
    analysis_utils.plot_autocorrelation(
        cf.set_index("L"), "Время", "Значение ковариации", "red"
    )

    st.divider()
    st.markdown("#### График кроскорреляции")
    cross_correlation = analysis.ccf(data, data_cross)
    analysis_utils.plot_cross_correlation(
        cross_correlation.set_index("L"), "Время", "Значение кроскорреляции", "red"
    )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
