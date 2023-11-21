import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import model, processing
from model import utils as model_utils

add_page_title()
show_pages_from_config()

model = model.Model()
processing = processing.Processing()


linear_trend_data = model_utils.get_linear_trend()
harm_data = model_utils.get_harm_process()

st.sidebar.divider()

non_linear_trend_data = model_utils.get_non_linear_trend()
polyharm_data = model_utils.get_polyharm_process()

addmodel_linear_harm = model.add_model(linear_trend_data, harm_data)
addmodel_non_linear_polyharm = model.add_model(non_linear_trend_data, polyharm_data)

st.markdown("#### Данные аддитивной модели линейного тренда и гармонического процесса")
st.line_chart(addmodel_linear_harm)

st.markdown("#### Данные после удаления линейного тренда")
harm_process = processing.antitrendlinear(addmodel_linear_harm)
st.line_chart(harm_process)

st.divider()
st.markdown(
    "#### Данные аддитивной модели нелинейного тренда и полигармонического процесса"
)
st.line_chart(addmodel_non_linear_polyharm)

st.markdown("#### Данные после удаления нелинейного тренда")
w_value = st.number_input("Введите значение W", value=10)
polyharm_process = processing.antitrendnonlinear(addmodel_non_linear_polyharm, w_value)
st.line_chart(polyharm_process)
