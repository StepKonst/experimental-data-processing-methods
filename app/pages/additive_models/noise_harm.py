import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from model import Model
from model import utils as model_utils
from processing import Processing

model = Model()
processing = Processing()


def main():
    add_page_title()
    show_pages_from_config()

    st.sidebar.title("Настройки")
    st.sidebar.subheader("Настройки шума")

    n_value, r_value, c_value, segment = model_utils.get_noise_value(n=1000, r=30.0)

    noise_data = model_utils.get_noise(n_value, r_value)
    noise_data = model.shift(noise_data, c_value, segment[0], segment[1])

    st.sidebar.subheader("Настройки гармонического процесса")
    n_harm, a_harm, f_harm, delta_t = model_utils.get_harm_value(
        a_value=10, f_value=5.0, delta_value=0.001
    )
    harm_data = model.harm(N=n_harm, A0=a_harm, f0=f_harm, delta_t=delta_t)

    addmodel_noise_harm = model.add_model(noise_data, harm_data)

    st.subheader("Данные аддитивной модели случайного шума и гармонического процесса")

    model_utils.plot_line_chart(
        addmodel_noise_harm, "Время", "Значение аддитивной модели", "purple"
    )

    st.subheader("Данные после удаления линейного тренда")

    result = processing.antitrendlinear(addmodel_noise_harm)

    model_utils.plot_line_chart(result, "Время", "Значение аддитивной модели", "purple")

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
