import numpy as np
import streamlit as st

import analysis


analysis = analysis.Analysis()


def distribution_density(data: np.ndarray):
    st.markdown("#### График плотности распределения")
    m_value_density = st.slider(
        "Выберите количество интервалов гистограммы",
        min_value=1,
        max_value=200,
        step=1,
        value=100,
    )
    hist_data = analysis.hist(data, m_value_density)
    st.bar_chart(hist_data.set_index("x"))
