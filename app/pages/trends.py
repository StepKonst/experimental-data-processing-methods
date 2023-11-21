import os
import sys

import pandas as pd
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import model, analysis, processing
from analysis import utils
from model import utils as model_utils

add_page_title()
show_pages_from_config()


st.title("Визуализация данных трендов")

model = model.Model()
analysis = analysis.Analysis()
processing = processing.Processing()

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

model_utils.get_dataframe(statistical_characteristics=statistical_characteristics)

st.divider()
st.markdown("#### Данные после удаления в них смещения")
anti_shift_data = processing.antishift(data=data)
st.line_chart(anti_shift_data)

st.divider()
utils.distribution_density(data)
