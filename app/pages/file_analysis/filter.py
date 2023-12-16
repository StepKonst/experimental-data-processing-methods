import os
import sys
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from analysis import Analysis
from processing import Processing

add_page_title()
show_pages_from_config()


def create_chart(data, color="orange"):
    chart = alt.Chart(data).mark_line(color=color).encode(x="index", y="value")
    return chart


def main():
    st.sidebar.title("Настройки")

    analysis = Analysis()
    processing = Processing()

    fc_value = st.sidebar.number_input(
        "Выберите значение fc", min_value=1, max_value=100, step=1, value=50
    )
    dt_value = st.sidebar.number_input(
        "Выберите значение dt", min_value=0.0001, max_value=1.0, step=0.001, value=0.002
    )
    m_value = st.sidebar.number_input(
        "Выберите значение m", min_value=1, max_value=100, step=1, value=64
    )
    fc1_value = st.sidebar.number_input(
        "Выберите значение fc1", min_value=1, max_value=100, step=1, value=35
    )
    fc2_value = st.sidebar.number_input(
        "Выберите значение fc2", min_value=1, max_value=100, step=1, value=75
    )

    file_path = "files/pgp_dt0005.dat"

    with open(file_path, "rb") as file:
        binary_data = file.read()

    float_data = np.frombuffer(binary_data, dtype=np.float32)

    file_data_furier = analysis.Fourier(float_data, len(float_data))
    file_data_X_n = analysis.spectrFourier(
        [i for i in range(len(float_data))], len(float_data), dt_value
    )

    lpw = processing.lpf(fc1_value, dt_value, m_value)
    ref_lpw = processing.reflect_lpf(lpw)
    hpw = processing.hpf(fc2_value, dt_value, m_value)
    bpw = processing.bpf(fc1_value, fc2_value, dt_value, m_value)
    bsw = processing.bsf(fc1_value, fc2_value, dt_value, m_value)

    tf_lpw = analysis.frequencyResponse(ref_lpw, 2 * m_value + 1)
    tf_hpw = analysis.frequencyResponse(hpw, 2 * m_value + 1)
    tf_bpw = analysis.frequencyResponse(bpw, 2 * m_value + 1)
    tf_bsw = analysis.frequencyResponse(bsw, 2 * m_value + 1)
    new_X_n = analysis.spectrFourier(
        [i for i in range(2 * m_value + 1)], 2 * m_value + 1, dt_value
    )

    convolution_lpf = analysis.convolution(
        float_data, ref_lpw, len(float_data), 2 * m_value + 1
    )
    convolution_hpf = analysis.convolution(
        float_data, hpw, len(float_data), 2 * m_value + 1
    )
    convolution_bpf = analysis.convolution(
        float_data, bpw, len(float_data), 2 * m_value + 1
    )
    convolution_bsf = analysis.convolution(
        float_data, bsw, len(float_data), 2 * m_value + 1
    )

    convolution_lpf_furier = analysis.Fourier(convolution_lpf, len(convolution_lpf))
    convolution_hpf_furier = analysis.Fourier(convolution_hpf, len(convolution_lpf))
    convolution_bpf_furier = analysis.Fourier(convolution_bpf, len(convolution_lpf))
    convolution_bsf_furier = analysis.Fourier(convolution_bsf, len(convolution_lpf))

    # График сигнала
    st.subheader("График сигнала")
    chart_signal = alt.Chart(
        pd.DataFrame({"Time": np.arange(len(float_data)), "Signal": float_data})
    )
    st.altair_chart(
        chart_signal.mark_line(color="green").encode(x="Time:Q", y="Signal:Q"),
        use_container_width=True,
    )

    st.markdown("## ФНЧ")

    # График спектра сигнала
    st.subheader("График спектра сигнала")
    df_spectre = pd.DataFrame(
        {"Frequency": file_data_X_n, "Amplitude": file_data_furier}
    )
    df_spectre_half = df_spectre[df_spectre["Frequency"] <= max(file_data_X_n) / 2]
    chart_spectre = alt.Chart(df_spectre_half)
    st.altair_chart(
        chart_spectre.mark_line(color="green").encode(x="Frequency:Q", y="Amplitude:Q"),
        use_container_width=True,
    )

    # График функции LPF
    st.subheader("График функции LPF")
    df_lpf = pd.DataFrame({"Frequency": new_X_n, "Amplitude": tf_lpw})
    df_lpf_half = df_lpf[df_lpf["Frequency"] <= max(new_X_n) / 2]
    chart_lpf = alt.Chart(df_lpf_half)
    st.altair_chart(
        chart_lpf.mark_line(color="green").encode(x="Frequency:Q", y="Amplitude:Q"),
        use_container_width=True,
    )

    # График свертки сигнала и функции LPF
    st.subheader("График свертки сигнала и функции LPF")
    chart_convolution = alt.Chart(
        pd.DataFrame(
            {"Time": np.arange(len(convolution_lpf)), "Convolution": convolution_lpf}
        )
    )
    st.altair_chart(
        chart_convolution.mark_line(color="green").encode(
            x="Time:Q", y="Convolution:Q"
        ),
        use_container_width=True,
    )

    # График спектра свертки
    st.subheader("График спектра свертки")
    df_convolution_spectre = pd.DataFrame(
        {"Frequency": file_data_X_n, "Amplitude": convolution_lpf_furier}
    )
    df_convolution_spectre_half = df_convolution_spectre[
        df_convolution_spectre["Frequency"] <= max(file_data_X_n) / 2
    ]
    chart_convolution_spectre = alt.Chart(df_convolution_spectre_half)
    st.altair_chart(
        chart_convolution_spectre.mark_line(color="green").encode(
            x="Frequency:Q", y="Amplitude:Q"
        ),
        use_container_width=True,
    )
    st.divider()

    st.markdown("## ФВЧ")

    # Создаем DataFrame для altair
    df_file_data = pd.DataFrame(
        {"Time": np.arange(len(float_data)), "Signal": float_data}
    )
    df_spectre = pd.DataFrame(
        {"Frequency": file_data_X_n, "Amplitude": file_data_furier}
    )
    df_spectre_half = df_spectre[df_spectre["Frequency"] <= max(file_data_X_n) / 2]
    df_tf_hpw = pd.DataFrame({"Frequency": new_X_n, "Amplitude": tf_hpw})
    df_tf_hpw_half = df_tf_hpw[df_tf_hpw["Frequency"] <= max(new_X_n) / 2]
    df_convolution_hpf = pd.DataFrame(
        {"Time": np.arange(len(convolution_hpf)), "Convolution": convolution_hpf}
    )
    df_convolution_spectre = pd.DataFrame(
        {"Frequency": file_data_X_n, "Amplitude": convolution_hpf_furier}
    )
    df_convolution_spectre_half = df_convolution_spectre[
        df_convolution_spectre["Frequency"] <= max(file_data_X_n) / 2
    ]

    # Создаем графики с использованием Altair
    chart_signal = (
        alt.Chart(df_file_data)
        .mark_line(color="green")
        .encode(x="Time:Q", y="Signal:Q")
    )
    chart_spectre = (
        alt.Chart(df_spectre_half)
        .mark_line(color="green")
        .encode(x="Frequency:Q", y="Amplitude:Q")
    )
    chart_tf_hpw = (
        alt.Chart(df_tf_hpw_half)
        .mark_line(color="green")
        .encode(x="Frequency:Q", y="Amplitude:Q")
    )
    chart_convolution = (
        alt.Chart(df_convolution_hpf)
        .mark_line(color="green")
        .encode(x="Time:Q", y="Convolution:Q")
    )
    chart_convolution_spectre = (
        alt.Chart(df_convolution_spectre_half)
        .mark_line(color="green")
        .encode(x="Frequency:Q", y="Amplitude:Q")
    )

    # Отображаем графики в Streamlit
    st.subheader("График сигнала")
    st.altair_chart(chart_signal, use_container_width=True)

    st.subheader("График спектра сигнала")
    st.altair_chart(chart_spectre, use_container_width=True)

    st.subheader("График функции HPF")
    st.altair_chart(chart_tf_hpw, use_container_width=True)

    st.subheader("График свертки сигнала и функции HPF")
    st.altair_chart(chart_convolution, use_container_width=True)

    st.subheader("График спектра свертки")
    st.altair_chart(chart_convolution_spectre, use_container_width=True)

    st.divider()

    st.markdown("## ПФ")

    # Создаем DataFrame для altair
    df_file_data = pd.DataFrame(
        {"Time": np.arange(len(float_data)), "Signal": float_data}
    )
    df_spectre = pd.DataFrame(
        {"Frequency": file_data_X_n, "Amplitude": file_data_furier}
    )
    df_spectre_half = df_spectre[df_spectre["Frequency"] <= max(file_data_X_n) / 2]
    df_tf_bpw = pd.DataFrame({"Frequency": new_X_n, "Amplitude": tf_bpw})
    df_tf_bpw_half = df_tf_bpw[df_tf_bpw["Frequency"] <= max(new_X_n) / 2]
    df_convolution_bpf = pd.DataFrame(
        {"Time": np.arange(len(convolution_bpf)), "Convolution": convolution_bpf}
    )
    df_convolution_spectre = pd.DataFrame(
        {"Frequency": file_data_X_n, "Amplitude": convolution_bpf_furier}
    )
    df_convolution_spectre_half = df_convolution_spectre[
        df_convolution_spectre["Frequency"] <= max(file_data_X_n) / 2
    ]

    # Создаем графики с использованием Altair
    chart_signal = (
        alt.Chart(df_file_data)
        .mark_line(color="green")
        .encode(x="Time:Q", y="Signal:Q")
    )
    chart_spectre = (
        alt.Chart(df_spectre_half)
        .mark_line(color="green")
        .encode(x="Frequency:Q", y="Amplitude:Q")
    )
    chart_tf_bpw = (
        alt.Chart(df_tf_bpw_half)
        .mark_line(color="green")
        .encode(x="Frequency:Q", y="Amplitude:Q")
    )
    chart_convolution = (
        alt.Chart(df_convolution_bpf)
        .mark_line(color="green")
        .encode(x="Time:Q", y="Convolution:Q")
    )
    chart_convolution_spectre = (
        alt.Chart(df_convolution_spectre_half)
        .mark_line(color="green")
        .encode(x="Frequency:Q", y="Amplitude:Q")
    )

    # Отображаем графики в Streamlit
    st.subheader("График сигнала")
    st.altair_chart(chart_signal, use_container_width=True)

    st.subheader("График спектра сигнала")
    st.altair_chart(chart_spectre, use_container_width=True)

    st.subheader("График функции BPF")
    st.altair_chart(chart_tf_bpw, use_container_width=True)

    st.subheader("График свертки сигнала и функции BPF")
    st.altair_chart(chart_convolution, use_container_width=True)

    st.subheader("График спектра свертки")
    st.altair_chart(chart_convolution_spectre, use_container_width=True)

    st.divider()

    st.markdown("## РФ")

    # Создаем DataFrame для altair
    df_file_data = pd.DataFrame(
        {"Time": np.arange(len(float_data)), "Signal": float_data}
    )
    df_spectre = pd.DataFrame(
        {"Frequency": file_data_X_n, "Amplitude": file_data_furier}
    )
    df_spectre_half = df_spectre[df_spectre["Frequency"] <= max(file_data_X_n) / 2]
    df_tf_bsw = pd.DataFrame({"Frequency": new_X_n, "Amplitude": tf_bsw})
    df_tf_bsw_half = df_tf_bsw[df_tf_bsw["Frequency"] <= max(new_X_n) / 2]
    df_convolution_bsf = pd.DataFrame(
        {"Time": np.arange(len(convolution_bsf)), "Convolution": convolution_bsf}
    )
    df_convolution_spectre = pd.DataFrame(
        {"Frequency": file_data_X_n, "Amplitude": convolution_bsf_furier}
    )
    df_convolution_spectre_half = df_convolution_spectre[
        df_convolution_spectre["Frequency"] <= max(file_data_X_n) / 2
    ]

    # Создаем графики с использованием Altair
    chart_signal = (
        alt.Chart(df_file_data)
        .mark_line(color="green")
        .encode(x="Time:Q", y="Signal:Q")
    )
    chart_spectre = (
        alt.Chart(df_spectre_half)
        .mark_line(color="green")
        .encode(x="Frequency:Q", y="Amplitude:Q")
    )
    chart_tf_bsw = (
        alt.Chart(df_tf_bsw_half)
        .mark_line(color="green")
        .encode(x="Frequency:Q", y="Amplitude:Q")
    )
    chart_convolution = (
        alt.Chart(df_convolution_bsf)
        .mark_line(color="green")
        .encode(x="Time:Q", y="Convolution:Q")
    )
    chart_convolution_spectre = (
        alt.Chart(df_convolution_spectre_half)
        .mark_line(color="green")
        .encode(x="Frequency:Q", y="Amplitude:Q")
    )

    # Отображаем графики в Streamlit
    st.subheader("График сигнала")
    st.altair_chart(chart_signal, use_container_width=True)

    st.subheader("График спектра сигнала")
    st.altair_chart(chart_spectre, use_container_width=True)

    st.subheader("График функции BSF")
    st.altair_chart(chart_tf_bsw, use_container_width=True)

    st.subheader("График свертки сигнала и функции BSF")
    st.altair_chart(chart_convolution, use_container_width=True)

    st.subheader("График спектра свертки")
    st.altair_chart(chart_convolution_spectre, use_container_width=True)


if __name__ == "__main__":
    main()
