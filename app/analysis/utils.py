import numpy as np
import streamlit as st

import analysis


analysis = analysis.Analysis()


def distribution_density(data: np.ndarray, M: int):
    st.markdown("### График плотности распределения")
    hist_data = analysis.hist(data, M)
    st.bar_chart(hist_data.set_index("x"))
