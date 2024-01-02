import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from analysis import Analysis
from model import utils as model_utils
from processing import Processing

analysis = Analysis()
processing = Processing()

add_page_title()
show_pages_from_config()


def main():
    st.sidebar.title("Настройки")

    fc_value = st.sidebar.number_input(
        "Выберите значение fc", min_value=1, max_value=100, step=1, value=50
    )
    dt_value = st.sidebar.number_input(
        "Выберите значение dt", min_value=0.0001, max_value=1.0, step=0.001, value=0.002
    )
    m_value = st.sidebar.number_input(
        "Выберите значение m", min_value=1, max_value=500, step=1, value=64
    )
    fc1_value = st.sidebar.number_input(
        "Выберите значение fc1", min_value=1, max_value=100, step=1, value=35
    )
    fc2_value = st.sidebar.number_input(
        "Выберите значение fc2", min_value=1, max_value=100, step=1, value=75
    )

    lpw = processing.lpf(fc_value, m_value, dt_value)
    ref_lpw = processing.reflect_lpf(lpw)
    hpf = processing.hpf(fc_value, m_value, dt_value)
    bpf = processing.bpf(fc1_value, fc2_value, m_value, dt_value)
    bsf = processing.bsf(fc1_value, fc2_value, m_value, dt_value)

    tf_ref_lpw = analysis.frequencyResponse(ref_lpw, 2 * m_value + 1)
    tf_hpf = analysis.frequencyResponse(hpf, 2 * m_value + 1)
    tf_bpf = analysis.frequencyResponse(bpf, 2 * m_value + 1)
    tf_bsf = analysis.frequencyResponse(bsf, 2 * m_value + 1)
    new_X_n = analysis.spectrFourier(
        [i for i in range(2 * m_value + 1)], 2 * m_value + 1, dt_value / 2
    )

    st.subheader("График импульсной реакции фильтра низких частот")
    model_utils.plot_line_chart(
        param1=range(len(lpw)),
        param2=lpw,
        x_label="Время",
        y_label="Значение импульсной реакции",
        color="darkorange",
        width=2,
    )

    st.subheader("График фильтра низких частот (2 * m + 1 Potter)")
    model_utils.plot_line_chart(
        param1=range(len(ref_lpw)),
        param2=ref_lpw,
        x_label="Время",
        y_label="Амплитуда импульсной реакции",
        color="darkorange",
        width=2,
    )

    st.subheader("График частотной характеристики LP Filter")
    new_X_n = new_X_n[: len(new_X_n) // 2]
    tf_ref_lpw = tf_ref_lpw[: len(tf_ref_lpw) // 2]
    model_utils.plot_line_chart(
        param1=new_X_n,
        param2=tf_ref_lpw,
        x_label="Частота",
        y_label="Амплитуда импульсной реакции",
        color="darkorange",
        width=2,
    )

    st.subheader("График фильтра высоких частот ФВЧ")
    model_utils.plot_line_chart(
        param1=range(len(hpf)),
        param2=hpf,
        x_label="Время",
        y_label="Амплитуда импульсной реакции",
        color="darkorange",
        width=2,
    )

    st.subheader("График частотной характеристики фильтра высоких частот")
    tf_hpf = tf_hpf[: len(tf_hpf) // 2]
    model_utils.plot_line_chart(
        param1=new_X_n,
        param2=tf_hpf,
        x_label="Частота",
        y_label="Амплитуда импульсной реакции",
        color="darkorange",
        width=2,
    )

    st.subheader("График полосового фильтра ПФ")
    model_utils.plot_line_chart(
        param1=range(len(bpf)),
        param2=bpf,
        x_label="Время",
        y_label="Амплитуда импульсной реакции",
        color="darkorange",
        width=2,
    )

    st.subheader("График частотной характеристики полосового фильтра")
    tf_bpf = tf_bpf[: len(tf_bpf) // 2]
    model_utils.plot_line_chart(
        param1=new_X_n,
        param2=tf_bpf,
        x_label="Частота",
        y_label="Амплитуда импульсной реакции",
        color="darkorange",
        width=2,
    )

    st.subheader("График режекторного фильтра РФ")
    model_utils.plot_line_chart(
        param1=range(len(bsf)),
        param2=bsf,
        x_label="Время",
        y_label="Амплитуда импульсной реакции",
        color="darkorange",
        width=2,
    )

    st.subheader("График частотной характеристики режекторного фильтра")
    tf_bsf = tf_bsf[: len(tf_bsf) // 2]
    model_utils.plot_line_chart(
        param1=new_X_n,
        param2=tf_bsf,
        x_label="Частота",
        y_label="Амплитуда импульсной реакции",
        color="darkorange",
        width=2,
    )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
