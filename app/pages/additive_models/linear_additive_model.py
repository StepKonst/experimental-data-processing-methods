import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import model
import processing
from model import utils as model_utils

add_page_title()
show_pages_from_config()

model = model.Model()
processing = processing.Processing()


def main():
    st.sidebar.title("Настройки")

    st.sidebar.subheader("Настройки линейного тренда")
    linear_trend_type = st.sidebar.selectbox(
        "Выберите тип линейного тренда",
        [
            "Линейно восходящий тренд",
            "Линейно нисходящий тренд",
        ],
    )

    a_value, b_value, N_value = model_utils.get_trend(n=1500)
    _, linear_trend_data = model.trend(linear_trend_type, a_value, b_value, N_value)

    st.sidebar.subheader("Настройки гармонического процесса")
    n_harm, a_harm, f_harm, delta_t = model_utils.get_harm_value()
    harm_data = model.harm(N=n_harm, A0=a_harm, f0=f_harm, delta_t=delta_t)

    st.sidebar.divider()
    st.sidebar.subheader("Настройки нелинейного тренда")
    non_linear_trend_data = model_utils.get_nonlinear_trend(n_value=1000)

    st.sidebar.subheader("Настройка полигармонического процесса")
    polyharm_n_value, a_f_values, polyharm_delta_t = model_utils.get_polyharm_value()

    polyharm_data = model.polyharm(
        N=polyharm_n_value, a_f_data=a_f_values, delta_t=polyharm_delta_t
    )

    if polyharm_data is None:
        st.error(
            "Некоректное значение временного интервала для полигармонического процесса"
        )
        sys.exit()

    addmodel_linear_harm = model.add_model(linear_trend_data, harm_data)
    addmodel_non_linear_polyharm = model.add_model(non_linear_trend_data, polyharm_data)

    st.subheader("Данные аддитивной модели линейного тренда и гармонического процесса")
    model_utils.plot_line_chart(
        range(len(addmodel_linear_harm)),
        addmodel_linear_harm,
        "Время",
        "Значение",
        "fuchsia",
        width=2,
    )

    st.subheader("Данные после удаления линейного тренда")
    harm_process = processing.antitrendlinear(addmodel_linear_harm)
    model_utils.plot_line_chart(
        range(len(harm_process)), harm_process, "Время", "Значение", "fuchsia", width=2
    )

    st.divider()
    st.subheader(
        "Данные аддитивной модели нелинейного тренда и полигармонического процесса"
    )
    model_utils.plot_line_chart(
        range(len(addmodel_non_linear_polyharm)),
        addmodel_non_linear_polyharm,
        "Время",
        "Значение",
        "fuchsia",
        width=2,
    )

    st.subheader("Данные после удаления нелинейного тренда")
    w_value = st.number_input("Введите значение W", value=10)
    polyharm_process = processing.antitrendnonlinear(
        addmodel_non_linear_polyharm, w_value
    )
    model_utils.plot_line_chart(
        range(len(polyharm_process)),
        polyharm_process,
        "Время",
        "Значение",
        "fuchsia",
        width=2,
    )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
