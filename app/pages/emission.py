import os
import sys

import pandas as pd
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
    'Выберите значение "R"', min_value=1.0, max_value=100.0, step=0.5, value=10.0
)
m_value = st.slider(
    'Выберите значение "M"',
    min_value=1,
    max_value=50,
    step=1,
    value=n_value // 100,
)
rs_value = st.slider(
    'Выберите значение "Rs"',
    min_value=0.1,
    max_value=5.0,
    step=0.1,
    value=m_value / 100 * 10,
)

emission_data, data_positions = model.spiles(n_value, m_value, r_value, rs_value)

st.line_chart(emission_data)

st.sidebar.dataframe(
    pd.DataFrame(
        {
            "Позиции": data_positions.get("Позиция"),
            "Значения": data_positions.get("Значения"),
        }
    ),
    width=300,
)
