import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import analysis, model
from analysis import utils
from model import utils as model_utils

model = model.Model()
analysis = analysis.Analysis()

add_page_title()
show_pages_from_config()


n_value = st.sidebar.number_input(
    'Выберите значение "N"', min_value=1, max_value=100000, step=1, value=10000
)
r_value = st.sidebar.number_input(
    'Выберите значение "R"', min_value=1.0, max_value=5000.0, step=0.5, value=1000.0
)

c_value = st.sidebar.number_input(
    "Выберите смещение C", min_value=0.0, max_value=10000.0, step=1.0, value=0.0
)
segment = st.sidebar.slider(
    "Выберите сегмент для смещения",
    min_value=1,
    max_value=n_value,
    value=(10, 1000),
)

# Генерация шума
noise_data = model_utils.get_my_noise(n_value=n_value, r_value=r_value)
# Шум для кросскорреляции
_, noise_data_cross = model.noise(n_value, r_value)
# Смещение для шумов
data = model.shift(noise_data, c_value, segment[0], segment[1])
# Смещение для шумов кросскорреляции
data_cross = model.shift(noise_data_cross, c_value, segment[0], segment[1])
# Статистические характеристики
statistical_characteristics = analysis.statistics(data)

st.sidebar.success(f"Выбранный отрезок: [{segment[0]}, {segment[1]}]")

st.markdown(
    "#### Данные для случайного шума с использованием несложного генератора случайных чисел:"
)
st.line_chart(data)
model_utils.get_dataframe(statistical_characteristics)

m = st.number_input(
    "Выберите количество сегментов для шума с использованием несложного генератора случайных чисел:",
    step=1,
    value=5,
    max_value=50,
)
st.success(analysis.stationarity(data, m))

st.divider()

utils.distribution_density(data)

st.divider()

st.markdown("#### Графики Автокорреляционной или Ковариационной функций")

func_type = st.selectbox(
    "Выберите тип функции",
    [
        "Автокорреляционная функция",
        "Ковариационная функция",
    ],
)

acf = analysis.acf(data, func_type)
st.line_chart(acf.set_index("L"))

st.divider()

st.markdown("#### График кроскорреляции")

cross_correlation = analysis.ccf(data, data_cross)
st.line_chart(cross_correlation.set_index("L"))
