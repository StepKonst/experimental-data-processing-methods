import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import analysis, model
from analysis import utils

model = model.Model()
analysis = analysis.Analysis()

add_page_title()
show_pages_from_config()

st.sidebar.markdown("### Настройка для визуализации гармонического процесса")
n_value = st.sidebar.number_input(
    "Выберите значение N",
    min_value=1,
    max_value=100000,
    step=1,
    value=1000,
)

a_value = st.sidebar.number_input(
    "Выберите значение A0",
    min_value=1,
    max_value=1000,
    step=1,
    value=100,
)

f_value = st.sidebar.number_input(
    "Выберите значение f0",
    min_value=0.1,
    max_value=600.0,
    step=100.0,
    value=15.0,
)

delta_t = st.sidebar.number_input(
    "Выберите значение delta_t",
    min_value=0.0,
    max_value=0.1,
    step=0.001,
    value=0.001,
)

harm_data = model.harm(N=n_value, A0=a_value, f0=f_value, delta_t=delta_t)

# Для процесса кроскорреляции
harm_data_cross = model.harm(N=n_value, A0=22, f0=33, delta_t=delta_t)

if harm_data is None:
    st.error("Некоректное значение временного интервала для гармонического процесса")
    sys.exit()

st.markdown("#### Гармонический процесс")
st.line_chart(harm_data)

st.divider()

utils.distribution_density(harm_data)

st.divider()

st.markdown("#### Графики Ковариационной и Автокорреляционной функций")

func_type = st.selectbox(
    "Выберите тип функции",
    [
        "Автокорреляционная функция",
        "Ковариационная функция",
    ],
)

acf = analysis.acf(harm_data, func_type)
st.line_chart(acf.set_index("L"))

st.divider()

# Кросскорреляция
st.markdown("#### График кросскорреляции")

cross_correlation = analysis.ccf(harm_data, harm_data_cross)
st.line_chart(cross_correlation.set_index("L"))

st.divider()

st.markdown("#### График амплитудного спектра Фурье гармонического процесса")
harm_spectr = analysis.spectr_fourier(harm_data, dt=delta_t)
st.line_chart(harm_spectr.set_index("f"))

st.divider()

l_values = [24, 124, 224]
harm_data_n = model.harm(N=1024, A0=100, f0=15.0, delta_t=0.001)
for L in l_values:
    st.markdown(f"#### График амплитудного спектра Фурье с окном L={L}")
    harm_spectr = analysis.spectr_fourier_window(harm_data_n, dt=delta_t, L=L)
    st.line_chart(harm_spectr.set_index("f"))
