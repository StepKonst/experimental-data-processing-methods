import os
import sys

import plotly.graph_objects as go
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import model
from model import utils as model_utils

add_page_title()
show_pages_from_config()

model = model.Model()


def main():
    st.markdown(
        """
        На этой странице представлен график кусочной функции, состоящей из 2-х, 3-х или 4-х трендов.
        
        Для настройки используйте боковую панель.

        #### Настройки
        - **Выберите несколько трендов:** Выберите несколько трендов для визуализации.
        - **Выберите значения параметров:** Выберите значения параметров для трендов.
        
        #### График кусочной функции

        График ниже показывает визуализацию кусочной функции, которая состоит из нескольких 
        трендов. Вы можете выбирать различные типы трендов и наблюдать изменения на графике 
        в режиме реального времени.


        """
    )

    st.sidebar.title("Настройки")

    trend_type = st.sidebar.multiselect(
        "Выберите два, три или даже четыре тренда",
        [
            "Линейно восходящий тренд",
            "Линейно нисходящий тренд",
            "Нелинейно восходящий тренд",
            "Нелинейно нисходящий тренд",
        ],
    )
    a_value, b_value, N_value = model_utils.get_trend()
    time, data = model.combined_trend(trend_type, a_value, b_value, N_value)

    if data is None:
        st.error("Выберите тренды в боковом меню")
    else:
        st.sidebar.success(f"Выбранные тренды: {trend_type}")

        fig = go.Figure(
            data=go.Scatter(x=time, y=data, line=dict(color="yellow", width=3))
        )
        fig.update_layout(
            title="График кусочной функции",
            xaxis_title="Время",
            yaxis_title="Значение",
            hovermode="x",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
