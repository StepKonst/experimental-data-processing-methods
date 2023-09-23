import os
import sys

import pandas as pd
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import model

add_page_title()

show_pages_from_config()


st.title("Комбинированная визуализация данных трендов")

model = model.Model()

trend_type = st.sidebar.multiselect(
    "Выберите два, три или даже четыре тренда",
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

t, data = model.combined_trend(trend_type, a_value, b_value, N_value)

if data is None:
    st.error("Выберите тренды в боковом меню")
else:
    st.success(f"Выбранные тренды: {trend_type}")

    st.subheader("Данные о тенденциях:")
    st.line_chart(data)

    st.sidebar.subheader("Таблица данных тренда:")
    st.sidebar.dataframe(pd.DataFrame({"Время": t, "Data": data}), width=300)
