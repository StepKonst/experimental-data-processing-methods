import sys
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
        height=423,
    )


def get_harm_process():
    st.sidebar.markdown("### Настройка для гармонического процесса")
    n_harm = st.sidebar.number_input(
        "Выберите значение n",
        min_value=1,
        max_value=100000,
        step=1,
        value=1000,
    )
    a_harm = st.sidebar.number_input(
        "Выберите значение A0",
        min_value=1,
        max_value=1000,
        step=1,
        value=100,
    )
    f_harm = st.sidebar.number_input(
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
    harm_data = model.harm(N=n_harm, A0=a_harm, f0=f_harm, delta_t=delta_t)

    if harm_data is None:
        st.error(
            "Некоректное значение временного интервала для гармонического процесса"
        )
        sys.exit()

    return harm_data


def get_polyharm_process():
    st.sidebar.markdown("### Настройка для полигармонического процесса")

    polyharm_n_value = st.sidebar.number_input(
        "Выберите значение N для полигармонического процесса",
        min_value=1,
        max_value=100000,
        step=1,
        value=1000,
    )
    polyharm_a1 = st.sidebar.slider(
        "Выберите значение А1 (Амплитуды)",
        min_value=0,
        max_value=1000,
        step=1,
        value=100,
    )
    polyharm_a2 = st.sidebar.slider(
        "Выберите значение А2 (Амплитуды)",
        min_value=0,
        max_value=1000,
        step=1,
        value=15,
    )
    polyharm_a3 = st.sidebar.slider(
        "Выберите значение А3 (Амплитуды)",
        min_value=0,
        max_value=1000,
        step=1,
        value=20,
    )
    polyharm_f1 = st.sidebar.slider(
        "Выберите значение f1 (Частоты)",
        min_value=0,
        max_value=1000,
        step=1,
        value=33,
    )
    polyharm_f2 = st.sidebar.slider(
        "Выберите значение f2 (Частоты)",
        min_value=0,
        max_value=1000,
        step=1,
        value=5,
    )
    polyharm_f3 = st.sidebar.slider(
        "Выберите значение f3 (Частоты)",
        min_value=0,
        max_value=1000,
        step=1,
        value=170,
    )
    a_f_values = [
        {"A": polyharm_a1, "f": polyharm_f1},
        {"A": polyharm_a2, "f": polyharm_f2},
        {"A": polyharm_a3, "f": polyharm_f3},
    ]
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

    return polyharm_data


def get_linear_trend():
    st.sidebar.markdown("### Настройка для линейного тренда")
    linear_trend_type = st.sidebar.selectbox(
        "Выберите линейный тренд",
        [
            "Линейно восходящий тренд",
            "Линейно нисходящий тренд",
        ],
    )
    a_linear = st.sidebar.slider(
        "Выберите значение a для линейного тренда",
        min_value=0.01,
        max_value=1.0,
        step=0.01,
        value=0.1,
    )
    b_linear = st.sidebar.slider(
        "Выберите значение b для линейного тренда",
        min_value=0.01,
        max_value=1.0,
        step=0.01,
        value=0.1,
    )
    n_linear = st.sidebar.slider(
        "Выберите значение n для линейного тренда",
        min_value=1,
        max_value=1000,
        step=1,
        value=1000,
    )

    _, linear_trend_data = model.trend(linear_trend_type, a_linear, b_linear, n_linear)

    return linear_trend_data


def get_non_linear_trend():
    st.sidebar.markdown("### Настройка для нелинейного тренда")
    non_linear_trend_type = st.sidebar.selectbox(
        "Выберите нелинейный тренд",
        [
            "Нелинейно восходящий тренд",
            "Нелинейно нисходящий тренд",
        ],
    )
    a_non_linear = st.sidebar.slider(
        "Выберите значение a для нелинейного тренда",
        min_value=0.01,
        max_value=1.0,
        step=0.01,
        value=0.1,
    )
    b_non_linear = st.sidebar.slider(
        "Выберите значение b для нелинейного тренда",
        min_value=0.01,
        max_value=1.0,
        step=0.01,
        value=0.1,
    )
    n_non_linear = st.sidebar.slider(
        "Выберите значение n для нелинейного тренда",
        min_value=1,
        max_value=1000,
        step=1,
        value=1000,
    )

    _, non_linear_trend_data = model.trend(
        non_linear_trend_type, a_non_linear, b_non_linear, n_non_linear
    )

    return non_linear_trend_data
