import os
import sys

import pandas as pd
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import analysis
from analysis import utils
import model

model = model.Model()
analysis = analysis.Analysis()

add_page_title()
show_pages_from_config()


@st.cache_data
def get_data(n_value: int, r_value: float):
    _, noise = model.noise(n_value, r_value)
    _, my_noise = model.my_noise(n_value, r_value)
    return noise, my_noise


def get_dataframe(statistical_characteristics: dict):
    return st.dataframe(
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
        height=420,
    )


n_value = st.sidebar.number_input(
    'Выберите значение "N"', min_value=1, max_value=100000, step=1, value=10000
)
r_value = st.sidebar.number_input(
    'Выберите значение "R"', min_value=1.0, max_value=5000.0, step=0.5, value=1000.0
)

c_value = st.sidebar.number_input(
    "Выберите смещение C:", min_value=0.0, max_value=10000.0, step=1.0, value=0.0
)
segment = st.sidebar.slider(
    "Выберите сегмент для смещения",
    min_value=1,
    max_value=n_value,
    value=(10, 1000),
)

default_data, default_data_me = get_data(n_value, r_value)

st.sidebar.success(f"Выбранный отрезок: [{segment[0]}, {segment[1]}]")

data = model.shift(default_data, c_value, segment[0], segment[1])
data_me = model.shift(default_data_me, c_value, segment[0], segment[1])

statistical_characteristics = analysis.statistics(n_value, data)
statistical_characteristics_me = analysis.statistics(n_value, data_me)

st.markdown("### Данные для случайного шума:")
st.line_chart(data)
get_dataframe(statistical_characteristics)

m_value = st.number_input(
    "Выберите количество сегментов для случайного шума:",
    step=1,
    value=5,
    max_value=50,
)
st.success(analysis.stationarity(data, m_value))

m_value_density = st.sidebar.slider(
    "Выберите количество интервалов гистограммы процессов",
    min_value=1,
    max_value=200,
    step=1,
    value=100,
)

utils.distribution_density(data, m_value_density)

st.markdown(
    "### Данные для случайного шума с использованием несложного генератора случайных чисел:"
)
st.line_chart(data_me)

get_dataframe(statistical_characteristics_me)
m = st.number_input(
    "Выберите количество сегментов для шума с использованием несложного генератора случайных чисел:",
    step=1,
    value=5,
    max_value=50,
)
st.success(analysis.stationarity(data_me, m))

utils.distribution_density(data_me, m_value_density)
