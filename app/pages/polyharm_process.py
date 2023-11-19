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

polyharm_data = model.polyharm(
    N=polyharm_n_value,
    a_f_data=a_f_values,
    delta_t=polyharm_delta_t,
)

if polyharm_data is None:
    st.error(
        "Некоректное значение временного интервала для полигармонического процесса"
    )
    sys.exit()

st.markdown("#### Полигармонический процесс")
st.line_chart(polyharm_data)

st.divider()

utils.distribution_density(polyharm_data)

st.divider()

st.markdown("#### График амплитудного спектра Фурье")
polyharm_spectr = analysis.spectr_fourier(polyharm_data, polyharm_delta_t)
st.line_chart(polyharm_spectr.set_index("f"))

st.divider()

l_values = [24, 124, 224]
for L in l_values:
    st.markdown(f"#### График амплитудного спектра Фурье с окном L={L}")
    polyharm_spectr = analysis.spectr_fourier_window(
        polyharm_data, dt=polyharm_delta_t, L=L
    )
    st.line_chart(polyharm_spectr.set_index("f"))
