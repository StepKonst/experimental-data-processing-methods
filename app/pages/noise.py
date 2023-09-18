import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import model

add_page_title()

show_pages_from_config()

st.title("Визуализация данных случайного шума")

model = model.Model()

N_value = st.slider(
    'Выберите значение "N"', min_value=1, max_value=10000, step=1, value=1000
)

R_value = st.slider(
    'Выберите значение "R"', min_value=1.0, max_value=500.0, step=1.0, value=10.0
)

time_values, data = model.noise(N_value, R_value)
time_values_me, data_me = model.my_noise(N_value, R_value)

st.markdown("## Данные для случайного шума:")
st.line_chart(data)

st.markdown(
    "## Данные для случайного шума с использованием несложного генератора случайных чисел:"
)

st.line_chart(data_me)
