import pandas as pd
import streamlit as st

import model


model = model.Model()


@st.cache_data
def get_noise(n_value: int, r_value: float):
    _, noise = model.noise(n_value, r_value)
    return noise


@st.cache_data
def get_my_noise(n_value: int, r_value: float):
    _, my_noise = model.my_noise(n_value, r_value)
    return my_noise


def get_dataframe(statistical_characteristics: dict):
    return st.dataframe(
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
        height=420,
    )
