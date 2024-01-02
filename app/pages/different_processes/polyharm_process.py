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

    polyharm_n_value, a_f_values, polyharm_delta_t = model_utils.get_polyharm_value()

    polyharm_data = model.polyharm(
        N=polyharm_n_value, a_f_data=a_f_values, delta_t=polyharm_delta_t
    )

    if polyharm_data is None:
        st.error(
            "Некоректное значение временного интервала для полигармонического процесса"
        )
        sys.exit()

    st.markdown("#### Полигармонический процесс")
    model_utils.plot_line_chart(
        param1=range(len(polyharm_data)),
        param2=polyharm_data,
        x_label="Время",
        y_label="Значение",
        color="blue",
        width=2,
    )

    st.divider()
    analysis_utils.distribution_density(polyharm_data, "blue")

    st.divider()
    st.markdown("#### График амплитудного спектра Фурье")
    polyharm_spectr = analysis.spectr_fourier(polyharm_data, polyharm_delta_t)
    analysis_utils.plot_fourier_spectrum(
        polyharm_spectr[: len(polyharm_spectr) // 2], "Частота", "Амплитуда", "blue"
    )

    st.divider()
    l_values = [24, 124, 224]
    for L in l_values:
        st.markdown(f"#### График амплитудного спектра Фурье с окном L={L}")
        polyharm_spectr = analysis.spectr_fourier_window(
            polyharm_data, dt=polyharm_delta_t, L=L
        )
        analysis_utils.plot_fourier_spectrum(
            polyharm_spectr, "Частота", "Амплитуда", "blue"
        )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
