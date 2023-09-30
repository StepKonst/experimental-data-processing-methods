import os
import sys

import pandas as pd
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import analysis
import model

model = model.Model()
analysis = analysis.Analysis()

# Add page title and show pages from config
add_page_title()
show_pages_from_config()

# Set main section options
n_value = st.slider(
    'Выберите значение "N"', min_value=1, max_value=10000, step=1, value=1000
)
r_value = st.slider(
    'Выберите значение "R"', min_value=1.0, max_value=5000.0, step=0.5, value=100.0
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

    statistical_characteristics = analysis.statistics(n_value, data)
    statistical_characteristics_me = analysis.statistics(n_value, data_me)

    # Display charts
    st.markdown("### Данные для случайного шума:")
    st.line_chart(data)
    st.dataframe(
        pd.DataFrame(
            {
                "Минимальное значение": statistical_characteristics.get(
                    "Минимальное значение"
                ),
                "Максимальное значение": statistical_characteristics.get(
                    "Максимальное значение"
                ),
                "Среднее значение": statistical_characteristics.get("Среднее значение"),
                "Дисперсия": statistical_characteristics.get("Дисперсия"),
                "Стандартное отклонение": statistical_characteristics.get(
                    "Стандартное отклонение"
                ),
                "Ассиметрия": statistical_characteristics.get("Ассиметрия"),
                "Коэффициент ассиметрии": statistical_characteristics.get(
                    "Коэффициент ассиметрии"
                ),
                "Эксцесс": statistical_characteristics.get("Эксцесс"),
                "Куртозис": statistical_characteristics.get("Куртозис"),
                "Средний квадрат": statistical_characteristics.get("Средний квадрат"),
                "Среднеквадратическая ошибка": statistical_characteristics.get(
                    "Среднеквадратическая ошибка"
                ),
            },
            index=["Значения"],
        ).T,
        width=700,
    )

    m_value = st.number_input(
        "Выберите количество сегментов для случайного шума:",
        step=1,
        value=50,
        max_value=100,
    )
    st.success(analysis.stationarity(data, m_value))

    st.markdown(
        "### Данные для случайного шума с использованием несложного генератора случайных чисел:"
    )
    st.line_chart(data_me)

    st.dataframe(
        pd.DataFrame(
            {
                "Минимальное значение": statistical_characteristics_me.get(
                    "Минимальное значение"
                ),
                "Максимальное значение": statistical_characteristics_me.get(
                    "Максимальное значение"
                ),
                "Среднее значение": statistical_characteristics_me.get(
                    "Среднее значение"
                ),
                "Дисперсия": statistical_characteristics_me.get("Дисперсия"),
                "Стандартное отклонение": statistical_characteristics_me.get(
                    "Стандартное отклонение"
                ),
                "Ассиметрия": statistical_characteristics_me.get("Ассиметрия"),
                "Коэффициент ассиметрии": statistical_characteristics_me.get(
                    "Коэффициент ассиметрии"
                ),
                "Эксцесс": statistical_characteristics_me.get("Эксцесс"),
                "Куртозис": statistical_characteristics_me.get("Куртозис"),
                "Средний квадрат": statistical_characteristics_me.get(
                    "Средний квадрат"
                ),
                "Среднеквадратическая ошибка": statistical_characteristics_me.get(
                    "Среднеквадратическая ошибка"
                ),
            },
            index=["Значения"],
        ).T,
        width=700,
    )
    m = st.number_input(
        "Выберите количество сегментов для шума с использованием несложного генератора случайных чисел:",
        step=1,
        value=50,
        max_value=100,
    )
    st.success(analysis.stationarity(data_me, m))
