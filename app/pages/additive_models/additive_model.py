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

    linear_trend_type = st.sidebar.selectbox(
        "Выберите линейный тренд",
        [
            "Линейно восходящий тренд",
            "Линейно нисходящий тренд",
        ],
    )

    non_linear_trend_type = st.sidebar.selectbox(
        "Выберите нелинейный тренд",
        [
            "Нелинейно восходящий тренд",
            "Нелинейно нисходящий тренд",
        ],
    )

    _, linear_trend_data = model.trend(linear_trend_type, a=0.3, b=20, N=1000)
    harm_data = model.harm(N=1000, A0=5, f0=50, delta_t=0.001)

    _, non_linear_trend_data = model.trend(non_linear_trend_type, a=0.05, b=10, N=100)
    _, noise_data = model.noise(N=100, R=10.0)

    addmodel1 = model.add_model(linear_trend_data, harm_data)
    addmodel2 = model.add_model(non_linear_trend_data, noise_data)

    st.markdown(
        "#### Данные аддитивной модели линейного тренда и гармонического процесса"
    )
    model_utils.plot_line_chart(
        range(len(addmodel1)),
        addmodel1,
        "Время",
        "Значение аддитивной модели",
        color="fuchsia",
        width=2,
    )

    st.markdown("#### Данные аддитивной модели нелинейного тренда и шума")
    model_utils.plot_line_chart(
        range(len(addmodel2)),
        addmodel2,
        "Время",
        "Значение аддитивной модели",
        color="fuchsia",
        width=2,
    )

    multimodel1 = model.multi_model(linear_trend_data, harm_data)
    multimodel2 = model.multi_model(non_linear_trend_data, noise_data)

    st.divider()
    st.markdown(
        "#### Данные мультипликативной модели линейного тренда и гармонического процесса"
    )
    model_utils.plot_line_chart(
        range(len(multimodel1)),
        multimodel1,
        "Время",
        "Значение мультипликативной модели",
        color="fuchsia",
        width=2,
    )

    st.markdown("#### Данные мультипликативной модели нелинейного тренда и шума")
    model_utils.plot_line_chart(
        range(len(multimodel2)),
        multimodel2,
        "Время",
        "Значение мультипликативной модели",
        color="fuchsia",
        width=2,
    )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
