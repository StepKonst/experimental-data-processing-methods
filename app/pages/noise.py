import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import model

model = model.Model()

# Add page title and show pages from config
add_page_title()
show_pages_from_config()

# Set main section options
n_value = st.slider(
    'Выберите значение "N"', min_value=1, max_value=5000, step=1, value=1000
)
r_value = st.slider(
    'Выберите значение "R"', min_value=1.0, max_value=500.0, step=0.5, value=10.0
)

# Set sidebar options
c_value = st.sidebar.number_input("Выберите смещение C:", step=1.0, value=0.0)
n1_value = st.sidebar.slider(
    "Выберите значение N1", min_value=0, max_value=n_value, step=1, value=300
)
n2_value = st.sidebar.slider(
    "Выберите значение N2", min_value=1, max_value=n_value, step=1, value=500
)

_, default_data = model.noise(n_value, r_value)
_, default_data_me = model.my_noise(n_value, r_value)

# Validate N1 and N2 values
if n1_value >= n2_value:
    st.sidebar.error("Ошибка: N1 должно быть меньше N2")
else:
    st.sidebar.success(f"Выбранный отрезок: [{n1_value}, {n2_value}]")

    data = model.shift(default_data, c_value, n1_value, n2_value)
    data_me = model.shift(default_data_me, c_value, n1_value, n2_value)

    # Display charts
    st.markdown("### Данные для случайного шума:")
    st.line_chart(data)

    st.markdown(
        "### Данные для случайного шума с использованием несложного генератора случайных чисел:"
    )
    st.line_chart(data_me)
