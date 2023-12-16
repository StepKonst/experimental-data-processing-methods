import sys
from typing import Tuple

import model
import pandas as pd
import plotly.express as px
import streamlit as st

model = model.Model()


def get_trend(a: float = 0.1, b: float = 0.1, n: int = 100) -> Tuple:
    """
    A function that gets the trend values.

    Parameters:
        a (float): The value of parameter "a". Default is 0.1.
        b (float): The value of parameter "b". Default is 0.1.
        n (int): The value of parameter "n". Default is 100.

    Returns:
        Tuple: A tuple containing the values of "a", "b", and "n".
    """
    a_value = st.sidebar.number_input(
        'Выберите значение "a"',
        min_value=0.01,
        max_value=100.0,
        step=0.01,
        value=a,
    )
    b_value = st.sidebar.number_input(
        'Выберите значение "b"',
        min_value=0.01,
        max_value=100.0,
        step=0.01,
        value=b,
    )
    N_value = st.sidebar.number_input(
        'Выберите значение "N"', min_value=1, max_value=10000, step=1, value=n
    )

    return a_value, b_value, N_value


def get_noise_value(
    n: int = 10000, r: float = 1000.0, c: float = 0.0, segment: Tuple = (10, 1000)
) -> Tuple:
    """
    Returns the noise value based on the given parameters.

    Args:
        n (int): The number of values to generate. Default is 10000.
        r (float): The range of values to generate. Default is 1000.0.
        c (float): The offset value to add to the noise. Default is 0.0.
        segment (Tuple): The range of values to select from the generated noise. Default is (10, 1000).

    Returns:
        Tuple: A tuple containing the generated noise values.
    """
    n_value = st.sidebar.number_input(
        'Выберите значение "N"', min_value=1, max_value=100000, step=1, value=n
    )
    r_value = st.sidebar.number_input(
        'Выберите значение "R"', min_value=1.0, max_value=5000.0, step=0.5, value=r
    )

    c_value = st.sidebar.number_input(
        "Выберите смещение C", min_value=0.0, max_value=10000.0, step=1.0, value=c
    )
    segment = st.sidebar.slider(
        "Выберите сегмент для смещения",
        min_value=0,
        max_value=n_value,
        value=(10, n_value),
    )

    return n_value, r_value, c_value, segment


def plot_line_chart(data, x_label, y_label, color="red"):
    """
    Plots a line chart using the given data.

    Parameters:
    - data (list): The data points to be plotted.
    - x_label (str): The label for the x-axis.
    - y_label (str): The label for the y-axis.
    - color (str, optional): The color of the line. Defaults to "red".

    Returns:
    - None
    """
    fig = px.line(
        x=range(len(data)),
        y=data,
        labels={"x": x_label, "y": y_label},
    )
    fig.update_traces(line=dict(color=color, width=1))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode="x",
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_chart_two_params(param1, param2, x_label, y_label, color, width):
    fig = px.line(
        x=param1,
        y=param2,
        labels={"x": x_label, "y": y_label},
    )
    fig.update_traces(line=dict(color=color, width=width))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode="x",
    )
    st.plotly_chart(fig, use_container_width=True)


def get_emission_value():
    """
    Generates the emission value based on user-selected parameters.

    Returns:
        n_value (int): The value of parameter "N" selected by the user.
        r_value (float): The value of parameter "R" selected by the user.
        m_value (int): The value of parameter "M" selected by the user.
        rs_value (float): The value of parameter "Rs" calculated based on the user-selected "M" value.
    """
    n_value = st.sidebar.slider(
        'Выберите значение "N"', min_value=1, max_value=5000, step=1, value=1000
    )
    r_value = st.sidebar.slider(
        'Выберите значение "R"', min_value=1.0, max_value=100.0, step=0.5, value=10.0
    )
    m_value = st.sidebar.slider(
        'Выберите значение "M"',
        min_value=1,
        max_value=50,
        step=1,
        value=n_value // 100,
    )
    rs_value = st.sidebar.slider(
        'Выберите значение "Rs"',
        min_value=0.1,
        max_value=5.0,
        step=0.1,
        value=m_value / 100 * 10,
    )

    return n_value, r_value, m_value, rs_value


@st.cache_data
def get_noise(n_value: int, r_value: float):
    _, noise = model.noise(n_value, r_value)
    return noise


@st.cache_data
def get_my_noise(n_value: int, r_value: float):
    _, my_noise = model.my_noise(n_value, r_value)
    return my_noise


def get_dataframe(statistical_characteristics: dict):
    characteristics = {
        "Измеряемые признаки": [
            "Минимальное значение",
            "Максимальное значение",
            "Среднее значение",
            "Дисперсия",
            "Стандартное отклонение",
            "Ассиметрия",
            "Коэффициент ассиметрии",
            "Эксцесс",
            "Куртозис",
            "Средний квадрат",
            "Среднеквадратическая ошибка",
        ],
        "Значения": [
            statistical_characteristics.get("Минимальное значение"),
            statistical_characteristics.get("Максимальное значение"),
            statistical_characteristics.get("Среднее значение"),
            statistical_characteristics.get("Дисперсия"),
            statistical_characteristics.get("Стандартное отклонение"),
            statistical_characteristics.get("Ассиметрия"),
            statistical_characteristics.get("Коэффициент ассиметрии"),
            statistical_characteristics.get("Эксцесс"),
            statistical_characteristics.get("Куртозис"),
            statistical_characteristics.get("Средний квадрат"),
            statistical_characteristics.get("Среднеквадратическая ошибка"),
        ],
    }
    return st.dataframe(pd.DataFrame(characteristics), width=700, height=423)


def get_harm_value(
    n_value: int = 1000,
    a_value: int = 100,
    f_value: float = 15.0,
    delta_value: float = 0.001,
):
    n_harm = st.sidebar.number_input(
        'Выберите значение "N"',
        min_value=1,
        max_value=10000,
        step=1,
        value=n_value,
    )
    a_harm = st.sidebar.number_input(
        "Выберите значение амплитуды",
        min_value=1,
        max_value=1000,
        step=1,
        value=a_value,
    )
    f_harm = st.sidebar.number_input(
        "Выберите значение частоты",
        min_value=0.1,
        max_value=600.0,
        step=100.0,
        value=f_value,
    )
    delta_t = st.sidebar.number_input(
        'Выберите значение "delta_t"',
        min_value=0.0,
        max_value=0.1,
        step=0.001,
        value=delta_value,
    )

    return n_harm, a_harm, f_harm, delta_t


def get_polyharm_value(
    polyharm_n_value: int = 1000,
    polyharm_a1_value: int = 100,
    polyharm_a2_value: int = 15,
    polyharm_a3_value: int = 20,
    polyharm_f1_value: int = 33,
    polyharm_f2_value: int = 5,
    polyharm_f3_value: int = 170,
    polyharm_delta_t_value: float = 0.001,
):
    polyharm_n_value = st.sidebar.number_input(
        "Выберите значение N для полигармонического процесса",
        min_value=1,
        max_value=100000,
        step=1,
        value=polyharm_n_value,
    )
    polyharm_a1 = st.sidebar.number_input(
        "Выберите значение А1 (Амплитуды)",
        min_value=0,
        max_value=1000,
        step=1,
        value=polyharm_a1_value,
    )
    polyharm_a2 = st.sidebar.number_input(
        "Выберите значение А2 (Амплитуды)",
        min_value=0,
        max_value=1000,
        step=1,
        value=polyharm_a2_value,
    )
    polyharm_a3 = st.sidebar.number_input(
        "Выберите значение А3 (Амплитуды)",
        min_value=0,
        max_value=1000,
        step=1,
        value=polyharm_a3_value,
    )
    polyharm_f1 = st.sidebar.number_input(
        "Выберите значение f1 (Частоты)",
        min_value=0,
        max_value=1000,
        step=1,
        value=polyharm_f1_value,
    )
    polyharm_f2 = st.sidebar.number_input(
        "Выберите значение f2 (Частоты)",
        min_value=0,
        max_value=1000,
        step=1,
        value=polyharm_f2_value,
    )
    polyharm_f3 = st.sidebar.number_input(
        "Выберите значение f3 (Частоты)",
        min_value=0,
        max_value=1000,
        step=1,
        value=polyharm_f3_value,
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
        value=polyharm_delta_t_value,
    )

    return polyharm_n_value, a_f_values, polyharm_delta_t


def get_exponential_trend_data(a: float = 30.0, b: float = 1.0):
    a_value = st.sidebar.number_input(
        'Выберите значение "a"',
        min_value=0.01,
        max_value=100.0,
        step=0.01,
        value=a,
    )
    b_value = st.sidebar.number_input(
        'Выберите значение "b"',
        min_value=0.01,
        max_value=100.0,
        step=0.01,
        value=b,
    )

    return a_value, b_value


########################################################################
def get_harm_process(
    n_value: int = 1000,
    a_value: int = 100,
    f_value: float = 15.0,
    delta_value: float = 0.001,
):
    st.sidebar.markdown("Настройка для гармонического процесса")
    n_harm = st.sidebar.number_input(
        'Выберите значение "N"',
        min_value=1,
        max_value=10000,
        step=1,
        value=n_value,
    )
    a_harm = st.sidebar.number_input(
        "Выберите значение амплитуды",
        min_value=1,
        max_value=1000,
        step=1,
        value=a_value,
    )
    f_harm = st.sidebar.number_input(
        "Выберите значение частоты",
        min_value=0.1,
        max_value=600.0,
        step=100.0,
        value=f_value,
    )
    delta_t = st.sidebar.number_input(
        'Выберите значение "delta_t"',
        min_value=0.0,
        max_value=0.1,
        step=0.001,
        value=delta_value,
    )
    harm_data = model.harm(N=n_harm, A0=a_harm, f0=f_harm, delta_t=delta_t)

    if harm_data is None:
        st.error(
            "Некоректное значение временного интервала для гармонического процесса"
        )
        sys.exit()

    return harm_data


def get_polyharm_process():
    st.sidebar.markdown("Настройка для полигармонического процесса")

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
        "Выберите значение f1 (Частоты)", min_value=0, max_value=1000, step=1, value=33
    )
    polyharm_f2 = st.sidebar.slider(
        "Выберите значение f2 (Частоты)", min_value=0, max_value=1000, step=1, value=5
    )
    polyharm_f3 = st.sidebar.slider(
        "Выберите значение f3 (Частоты)", min_value=0, max_value=1000, step=1, value=170
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
        N=polyharm_n_value, a_f_data=a_f_values, delta_t=polyharm_delta_t
    )

    if polyharm_data is None:
        st.error(
            "Некоректное значение временного интервала для полигармонического процесса"
        )
        sys.exit()

    return polyharm_data


def get_linear_trend(a_value: float = 0.1, b_value: float = 0.1, n_value: int = 100):
    st.sidebar.markdown("Настройка для линейного тренда")
    linear_trend_type = st.sidebar.selectbox(
        "Выберите линейный тренд",
        [
            "Линейно восходящий тренд",
            "Линейно нисходящий тренд",
        ],
    )
    a_linear = st.sidebar.number_input(
        "Выберите значение a для линейного тренда",
        min_value=0.01,
        max_value=50.0,
        step=0.01,
        value=a_value,
    )
    b_linear = st.sidebar.number_input(
        "Выберите значение b для линейного тренда",
        min_value=0.01,
        max_value=50.0,
        step=0.01,
        value=b_value,
    )
    n_linear = st.sidebar.number_input(
        "Выберите значение n для линейного тренда",
        min_value=1,
        max_value=1000,
        step=1,
        value=n_value,
    )

    _, linear_trend_data = model.trend(linear_trend_type, a_linear, b_linear, n_linear)

    return linear_trend_data


def get_nonlinear_trend(
    a_value: float = 0.01, b_value: float = 0.05, n_value: int = 100
):
    non_linear_trend_type = st.sidebar.selectbox(
        "Выберите нелинейный тренд",
        [
            "Нелинейно восходящий тренд",
            "Нелинейно нисходящий тренд",
        ],
    )
    a_non_linear = st.sidebar.number_input(
        "Выберите значение a для нелинейного тренда",
        min_value=0.01,
        max_value=50.0,
        step=0.01,
        value=a_value,
    )
    b_non_linear = st.sidebar.number_input(
        "Выберите значение b для нелинейного тренда",
        min_value=0.01,
        max_value=50.0,
        step=0.01,
        value=b_value,
    )
    n_non_linear = st.sidebar.number_input(
        "Выберите значение n для нелинейного тренда",
        min_value=1,
        max_value=2000,
        step=1,
        value=n_value,
    )

    _, non_linear_trend_data = model.trend(
        non_linear_trend_type,
        a_non_linear,
        b_non_linear,
        n_non_linear,
    )

    return non_linear_trend_data
