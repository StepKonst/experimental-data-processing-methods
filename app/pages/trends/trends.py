import os
import sys

import plotly.graph_objects as go
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import analysis
import model
from model import utils as model_utils

add_page_title()
show_pages_from_config()

model = model.Model()
analysis = analysis.Analysis()


def main():
    st.markdown(
        """
        На этой странице представлена визуализация трендовых данных. 
        Вы можете выбирать различные типы трендов и наблюдать изменения на графике в режиме реального времени. 
        
        Для настройки тренда используйте боковую панель.

        #### Настройки

        - **Выберите тренд:** Выберите тип тренда из бокового меню.
        - **Выберите значение а:** Значение а для выбранного тренда.
        - **Выберите значение b:** Значение b для выбранного тренда.
        - **Выберите значение N:** Значение N для выбранного тренда.
        
        #### График тренда

        График ниже демонстрирует временной ряд в зависимости от выбранного типа тренда.

        """
    )

    st.sidebar.title("Настройки")

    trend_type = st.sidebar.selectbox(
        "Выберите тренд",
        [
            "Линейно восходящий тренд",
            "Линейно нисходящий тренд",
            "Нелинейно восходящий тренд",
            "Нелинейно нисходящий тренд",
        ],
    )

    a_value, b_value, N_value = model_utils.get_trend()
    time, data = model.trend(trend_type, a_value, b_value, N_value)

    fig = go.Figure(data=go.Scatter(x=time, y=data, line=dict(color="yellow", width=3)))
    fig.update_layout(
        xaxis_title="Время",
        yaxis_title="Значение",
        hovermode="x",
    )
    st.plotly_chart(fig, use_container_width=True)

    statistical_characteristics = analysis.statistics(data)
    model_utils.get_dataframe(statistical_characteristics)

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
