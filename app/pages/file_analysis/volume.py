import os
import sys

import streamlit as st
import numpy as np
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import analysis
from model import utils as model_utils
from analysis import utils as analysis_utils

analysis = analysis.Analysis()

add_page_title()
show_pages_from_config()


def main():
    file_path = "files/pgp_dt0005.dat"

    with open(file_path, "rb") as file:
        binary_data = file.read()

    float_data = np.frombuffer(binary_data, dtype=np.float32)

    st.subheader("График сигнала")
    model_utils.plot_line_chart(
        param1=range(len(float_data)),
        param2=float_data,
        x_label="Время",
        y_label="Значение сигнала",
        color="limegreen",
        width=2,
    )

    harm_spectr = analysis.spectr_fourier(float_data, dt=0.0005)
    st.subheader("График амплитудного спектра Фурье")
    analysis_utils.plot_fourier_spectrum(
        harm_spectr, "Частота", "Амплитуда", "limegreen"
    )


if __name__ == "__main__":
    main()
