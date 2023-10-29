import os
import sys

import streamlit as st
import numpy as np
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import analysis

analysis = analysis.Analysis()

add_page_title()
show_pages_from_config()

file_path = "pgp_dt0005.dat"

with open(file_path, "rb") as file:
    binary_data = file.read()

float_data = np.frombuffer(binary_data, dtype=np.float32)

st.markdown("#### График сигнала")
st.line_chart(float_data)

delta_t = st.sidebar.number_input(
    "Выберите значение delta_t",
    min_value=0.0,
    max_value=0.1,
    step=0.001,
    value=0.0005,
)

harm_spectr = analysis.spectr_fourier(float_data, delta_t)
st.markdown("#### График амплитудного спектра Фурье")
st.line_chart(harm_spectr.set_index("f"))
