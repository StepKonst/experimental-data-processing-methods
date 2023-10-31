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

st.sidebar.markdown("### Настройка для визуализации полигармонического процесса")

polyharm_n_value = st.sidebar.number_input(
    "Выберите значение N для полигармонического процесса",
    min_value=1,
    max_value=100000,
    step=1,
    value=1000,
)

# Значения амплитуды и частоты для полигармонического процесса
a_f_values = [{"A": 100, "f": 33}, {"A": 15, "f": 5}, {"A": 20, "f": 170}]

polyharm_delta_t = st.sidebar.number_input(
    "Выберите значение delta_t для полигармонического процесса",
    min_value=0.0,
    max_value=0.1,
    step=0.001,
    value=0.001,
)

harm_data = model.harm(N=n_value, A0=a_value, f0=f_value, delta_t=delta_t)
polyharm_data = model.polyharm(
    N=polyharm_n_value,
    a_f_data=a_f_values,
    delta_t=polyharm_delta_t,
)

# Для процесса кроскорреляции
harm_data_z = model.harm(N=n_value, A0=a_value, f0=f_value, delta_t=delta_t)
harm_data_y = model.harm(N=n_value, A0=22, f0=33, delta_t=delta_t)

if harm_data is None or polyharm_data is None:
    st.error(
        "Некоректное значение временного интервала для гармонического или полигармонического процесса"
    )
    sys.exit()

st.markdown("## Гармонический процесс")
st.line_chart(harm_data)

m_value = st.sidebar.slider(
    "Выберите количество интервалов гистограммы процессов",
    min_value=1,
    max_value=200,
    step=1,
    value=100,
)

utils.distribution_density(harm_data, m_value)

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

# Кросскорреляция
st.markdown("#### График кросскорреляции")

cross_correlation = analysis.ccf(harm_data, harm_data_z)
st.line_chart(cross_correlation.set_index("L"))


st.markdown("#### График амплитудного спектра Фурье гармонического процесса")
harm_spectr = analysis.spectr_fourier(harm_data, dt=delta_t)
st.line_chart(harm_spectr.set_index("f"))

l_values = [24, 124, 224]
harm_data_n = model.harm(N=1024, A0=100, f0=15.0, delta_t=0.001)
harm_but = st.button("График амплитудного спектра Фурье гармонического процесса")
if harm_but:
    for L in l_values:
        st.markdown(f"#### График амплитудного спектра Фурье с окном L={L}")
        harm_spectr = analysis.spectr_fourier_window(harm_data_n, dt=delta_t, L=L)
        st.line_chart(harm_spectr.set_index("f"))

st.divider()

st.markdown("## Полигармонический процесс")
st.line_chart(polyharm_data)

utils.distribution_density(polyharm_data, m_value)

st.markdown("#### График амплитудного спектра Фурье")
polyharm_spectr = analysis.spectr_fourier(polyharm_data, polyharm_delta_t)
st.line_chart(polyharm_spectr.set_index("f"))

polyharm_but = st.button(
    "График амплитудного спектра Фурье полигармонического процесса"
)
if polyharm_but:
    for L in l_values:
        st.markdown(f"#### График амплитудного спектра Фурье с окном L={L}")
        polyharm_spectr = analysis.spectr_fourier_window(
            polyharm_data, dt=polyharm_delta_t, L=L
        )
        st.line_chart(polyharm_spectr.set_index("f"))
