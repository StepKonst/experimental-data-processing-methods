import os
import sys

import pandas as pd
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import model, analysis
from analysis import utils

add_page_title()

show_pages_from_config()


st.title("Визуализация данных трендов")

model = model.Model()
analysis = analysis.Analysis()

trend_type = st.sidebar.selectbox(
    "Выберите тип тренда",
    [
        "Линейно восходящий тренд",
        "Линейно нисходящий тренд",
        "Нелинейно восходящий тренд",
        "Нелинейно нисходящий тренд",
    ],
)
a_value = st.slider(
    'Выберите значение "a"', min_value=0.01, max_value=1.0, step=0.01, value=0.1
)
b_value = st.slider(
    'Выберите значение "b"', min_value=0.01, max_value=1.0, step=0.01, value=0.1
)
N_value = st.slider(
    'Выберите значение "N"', min_value=1, max_value=1000, step=1, value=100
)

t, data = model.trend(trend_type, a_value, b_value, N_value)

st.subheader("Данные o тенденциях:")
st.line_chart(data)

st.sidebar.subheader("Таблица данных тренда:")
st.sidebar.dataframe(pd.DataFrame({"Время": t, "Data": data}), width=300)

statistical_characteristics = analysis.statistics(data)

st.dataframe(
    pd.DataFrame(
        {
            "Минимальное значение": statistical_characteristics.get(
                "Минимальное значение"
            ),
            "Максимальное значение": statistical_characteristics.get(
                "Максимальное значение"
            ),
            "Среднее значение": statistical_characteristics.get("Среднее значение"),
            "Дисперсия": statistical_characteristics.get("Дисперсия"),
            "Стандартное отклонение": statistical_characteristics.get(
                "Стандартное отклонение"
            ),
            "Ассиметрия": statistical_characteristics.get("Ассиметрия"),
            "Коэффициент ассиметрии": statistical_characteristics.get(
                "Коэффициент ассиметрии"
            ),
            "Эксцесс": statistical_characteristics.get("Эксцесс"),
            "Куртозис": statistical_characteristics.get("Куртозис"),
            "Средний квадрат": statistical_characteristics.get("Средний квадрат"),
            "Среднеквадратическая ошибка": statistical_characteristics.get(
                "Среднеквадратическая ошибка"
            ),
        },
        index=["Значения"],
    ).T,
    width=700,
)

utils.distribution_density(data)
