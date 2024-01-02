import os
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from model import Model
from model import utils as model_utils
from processing import Processing

model = Model()
processing = Processing()

add_page_title()
show_pages_from_config()


def main():
    st.markdown(
        "#### Данная страница демонстрирует эффект подавления случайного шума методом накопления."
    )

    st.sidebar.title("Настройки")

    n_value = st.sidebar.number_input(
        "Выберите значение N", min_value=1, max_value=100000, step=1, value=1000
    )

    r_value = st.sidebar.number_input(
        "Выберите значение R", min_value=1.0, max_value=5000.0, step=0.5, value=100.0
    )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")

    M_values = [1, 10, 100, 10000]

    for M in M_values:
        st.divider()
        st.markdown(f"#### График для M = {M}")

        noise = [model.noise(n_value, r_value) for _ in range(M)]
        anti_noise = processing.antiNoise(noise, n_value, M)
        std_deviation = np.std(anti_noise)

        model_utils.plot_line_chart(
            range(len(anti_noise)), anti_noise, "Время", "Значение шума", "red", width=1
        )

        st.markdown(f"**Стандартное отклонение равно:** {std_deviation:.4f}")

    M_values_std = list(range(1, 1001, 10))

    results = []
    for M in M_values_std:
        noise = [model.noise(n_value, r_value) for _ in range(M)]
        anti_noise = processing.antiNoise(noise, n_value, M)
        std_deviation = np.std(anti_noise)
        results.append({"M": M, "std_deviation": std_deviation})

    df_results = pd.DataFrame(results)

    st.divider()
    st.markdown("#### График зависимости стандартного отклонения от M")
    fig = px.line(df_results, x="M", y="std_deviation")
    fig.update_layout(
        xaxis_title="M", yaxis_title="Стандартное отклонение", hovermode="x"
    )
    fig.update_traces(line=dict(color="red", width=2))

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
