import analysis
import numpy as np
import plotly.express as px
import streamlit as st

analysis = analysis.Analysis()


def distribution_density(data: np.ndarray, color: str):
    st.markdown("#### График плотности распределения")
    m_value_density = st.slider(
        "Выберите количество интервалов гистограммы",
        min_value=1,
        max_value=200,
        step=1,
        value=100,
    )
    hist_data = analysis.hist(data, m_value_density)

    fig = px.bar(
        hist_data,
        x="x",
        y="y",
        labels={"x": "Значение", "y": "Плотность"},
        color_discrete_sequence=[color],
    )
    fig.update_layout(
        xaxis_title="Значение",
        yaxis_title="Плотность вероятности",
    )

    fig.update_traces(hovertemplate="Значение: %{x}<br>Плотность: %{y}")
    st.plotly_chart(fig, use_container_width=True)


def plot_cross_correlation(data, x_label, y_label, color="blue"):
    fig = px.line(
        x=data.index,
        y=data["CCF"],
        labels={"x": x_label, "y": y_label},
    )
    fig.update_traces(line=dict(color=color, width=2))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode="x",
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_autocorrelation(data, x_label, y_label, color="blue"):
    fig = px.line(
        x=data.index,
        y=data["AC"],
        labels={"x": x_label, "y": y_label},
    )
    fig.update_traces(line=dict(color=color, width=2))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode="x",
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_fourier_spectrum(data, x_label, y_label, color="blue"):
    fig = px.line(
        x=data["f"],
        y=data["|Xn|"],
        labels={"x": x_label, "y": y_label},
    )
    fig.update_traces(line=dict(color=color, width=2))
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode="x",
    )
    st.plotly_chart(fig, use_container_width=True)
