import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import model, processing

add_page_title()
show_pages_from_config()

model = model.Model()
processing = processing.Processing()

n_value = st.number_input(
    "Выберите значение N", min_value=1, max_value=100000, step=1, value=1000
)

st.sidebar.markdown("### Настройка для шума")
r_noise = st.sidebar.number_input(
    "Выберите значение R", min_value=1.0, max_value=5000.0, step=0.5, value=100.0
)
c_noise = st.sidebar.number_input(
    "Выберите смещение C", min_value=0.0, max_value=10000.0, step=1.0, value=0.0
)
segment = st.sidebar.slider(
    "Выберите сегмент для смещения",
    min_value=1,
    max_value=n_value,
    value=(10, n_value // 2),
)

st.sidebar.divider()
st.sidebar.markdown("### Настройка для выброса")
r_emission = st.sidebar.slider(
    "Выберите значение R", min_value=1.0, max_value=1000.0, step=0.5, value=50.0
)
m_emission = st.sidebar.slider(
    "Выберите значение M",
    min_value=1,
    max_value=50,
    step=1,
    value=n_value // 100,
)
rs_emission = st.sidebar.slider(
    "Выберите значение Rs",
    min_value=0.1,
    max_value=5.0,
    step=0.1,
    value=m_emission / 100 * 10,
)

st.sidebar.divider()
st.sidebar.markdown("### Настройка для гармонического процесса")
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

_, noise_data = model.noise(n_value, r_noise)
shift_noise_data = model.shift(noise_data, c_noise, segment[0], segment[1])

emission_data, data_positions = model.spikes(
    n_value, m_emission, r_emission, rs_emission
)

harm_data = model.harm(N=n_value, A0=a_harm, f0=f_harm, delta_t=delta_t)

additive_noise_emission = model.add_model(emission_data, shift_noise_data)
additive_harm_emission = model.add_model(emission_data, harm_data)

st.markdown("#### Аддитивная модель данных шума и выброса")
st.line_chart(additive_noise_emission)

st.markdown(
    "#### Аддитивная модель данных шума и выброса после удаления неправдоподобных значений"
)
range_noise = st.number_input("Введите значение диапозона для модели шума", value=10)
anti_spike_noise = processing.antispike(additive_noise_emission, range_noise)
st.line_chart(anti_spike_noise)

st.divider()
st.markdown("#### Аддитивная модель данных гармонического процесса и выброса")
st.line_chart(additive_harm_emission)

st.markdown(
    "#### Аддитивная модель данных гармонического процесса и выброса после удаления неправдоподобных значений"
)
range_harm = st.number_input(
    "Введите значение диапозона для модели гармонического процесса", value=10
)
anti_spike_harm = processing.antispike(additive_harm_emission, range_harm)
st.line_chart(anti_spike_harm)
