import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import analysis
import model
from analysis import utils as analysis_utils
from model import utils as model_utils

model = model.Model()
analysis = analysis.Analysis()

add_page_title()
show_pages_from_config()


def main():
    st.sidebar.title("Настройки")

    n_value, a_value, f_value, delta_t = model_utils.get_harm_value()
    harm_data = model.harm(N=n_value, A0=a_value, f0=f_value, delta_t=delta_t)

    harm_data_cross = model.harm(N=n_value, A0=22, f0=33, delta_t=delta_t)

    if harm_data is None:
        st.error(
            "Некоректное значение временного интервала для гармонического процесса"
        )
        sys.exit()

    st.markdown("#### Гармонический процесс")
    model_utils.plot_line_chart(
        param1=range(len(harm_data)),
        param2=harm_data,
        x_label="Время",
        y_label="Значение",
        color="blue",
        width=2,
    )

    st.divider()
    analysis_utils.distribution_density(harm_data, "blue")

    st.divider()
    st.markdown("#### График Автокорреляционной функции")
    acf = analysis.acf(harm_data, "Автокорреляционная функция")
    analysis_utils.plot_autocorrelation(
        acf.set_index("L"), "Время", "Значение автокорреляции", "blue"
    )

    st.divider()
    st.markdown("#### График Ковариационной функции")
    cf = analysis.acf(harm_data, "Ковариационная функция")
    analysis_utils.plot_autocorrelation(
        cf.set_index("L"), "Время", "Значение ковариации", "blue"
    )

    st.divider()
    cross_correlation = analysis.ccf(harm_data, harm_data_cross)
    st.markdown("#### График кроскорреляции")
    analysis_utils.plot_cross_correlation(
        cross_correlation.set_index("L"), "Время", "Значение кроскорреляции", "blue"
    )

    st.divider()
    st.markdown("#### График амплитудного спектра Фурье гармонического процесса")
    harm_spectr = analysis.spectr_fourier(harm_data, dt=delta_t)
    analysis_utils.plot_fourier_spectrum(harm_spectr, "Частота", "Амплитуда", "blue")

    st.divider()
    l_values = [24, 124, 224]
    harm_data_n = model.harm(N=1024, A0=100, f0=15.0, delta_t=0.001)
    for L in l_values:
        st.markdown(f"#### График амплитудного спектра Фурье с окном L={L}")
        harm_spectr = analysis.spectr_fourier_window(harm_data_n, dt=delta_t, L=L)
        analysis_utils.plot_fourier_spectrum(
            harm_spectr, "Частота", "Амплитуда", "blue"
        )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
