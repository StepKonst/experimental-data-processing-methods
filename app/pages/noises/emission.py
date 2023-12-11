import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import model
from model import utils as model_utils

model = model.Model()

add_page_title()
show_pages_from_config()


def main():
    st.sidebar.title("Настройки")
    n_value, r_value, m_value, rs_value = model_utils.get_emission_value()
    emission_data = model.spikes(n_value, m_value, r_value, rs_value)[0]

    st.markdown("#### Данные выброса")
    model_utils.plot_line_chart(emission_data, "Время", "Значение выброса", "red")


if __name__ == "__main__":
    main()
