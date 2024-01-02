import os
import sys

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import analysis
import model
import processing
from analysis import utils as analysis_utils
from model import utils as model_utils

model = model.Model()
analysis = analysis.Analysis()
processing = processing.Processing()

add_page_title()
show_pages_from_config()


def main():
    st.markdown(
        """
        ## Визуализация случайного шума

        На этой странице представлена визуализация данных случайного шума. 
        
        Для настройки шума используйте боковую панель.

        ### Настройки

        - **Выберите значение "N":** Количество значений для генерации шума.
        - **Выберите значение "R":** Диапазон значений для генерации шума.
        - **Выберите смещение "C":** Значение смещения для добавления к шуму.
        - **Выберите сегмент для смещения:** Диапазон значений для смещения в сгенерированном шуме.

        """
    )

    st.sidebar.title("Настройки")
    n_value, r_value, c_value, segment = model_utils.get_noise_value()

    noise_data = model_utils.get_noise(n_value, r_value)
    noise_data_cross = model.noise(n_value, r_value)[1]

    shift_noise_data = model.shift(noise_data, c_value, segment[0], segment[1])
    data_cross = model.shift(noise_data_cross, c_value, segment[0], segment[1])

    statistical_characteristics = analysis.statistics(shift_noise_data)

    st.sidebar.success(f"Выбранный отрезок: [{segment[0]}, {segment[1]}]")

    st.markdown(
        """
        #### График случайного шума.
        
        График ниже демонстрирует сгенерированный по выбранным параметрам случайный шум.
        
        """
    )
    model_utils.plot_line_chart(
        range(len(shift_noise_data)),
        shift_noise_data,
        "Время",
        "Значение шума",
        "red",
        width=1,
    )

    st.markdown(
        """
        #### Статистические характеристики.
        
        В виде таблицы представлены самые популярные статистические характеристики для шума.
        
        """
    )
    model_utils.get_dataframe(statistical_characteristics)

    st.markdown(
        """
        
            #### Проверка шума на стационарность.
            
            В разделе "Проверка шума на стационарность" мы используем следующий подход. 
            Сначала мы разбиваем длину 𝑁 на 𝑀 равных отрезков и вычисляем среднее значение 
            (СЗ) 𝑥̅𝑖 и стандартное отклонение (СО) 𝜎𝑖 для каждого отрезка. Затем, путем полного 
            перебора всех пар отрезков, мы определяем величины их относительных изменений: 
            для СЗ - 𝛿𝑖𝑗 = 𝑥̅𝑖−𝑥̅𝑗 и для СО - 𝛿𝑖𝑗 = 𝜎𝑖−𝜎𝑗; где 𝑖≠𝑗; 𝑖,j=1,2,..,𝑀. Если величины 
            относительных изменений составляют менее 5% от диапазона значений шума, то мы 
            считаем процесс стационарным. В противном случае - нестационарным.
        
        """
    )
    m_value = st.number_input(
        "Выберите количество сегментов для шума",
        step=1,
        value=5,
        max_value=50,
    )
    st.success(analysis.stationarity(shift_noise_data, m_value))

    st.divider()
    st.markdown(
        """
        
            #### Данные после удаления в них смещения
            
            При обнаружении и удалении смещения в данных мы следуем следующему подходу. 
            Сначала находим среднее значение (центр рассеивания) данных и вычитаем его из всех 
            значений данных. Это позволяет удалить смещение и сделать данные центрированными.
                
        """
    )
    anti_shift_data = processing.antishift(shift_noise_data)
    model_utils.plot_line_chart(
        range(len(anti_shift_data)),
        anti_shift_data,
        "Время",
        "Значение шума",
        "red",
        width=1,
    )

    st.divider()
    analysis_utils.distribution_density(shift_noise_data, "red")

    st.divider()
    st.markdown("#### График Автокорреляционной функции")
    acf = analysis.acf(shift_noise_data, "Автокорреляционная функция")
    analysis_utils.plot_autocorrelation(
        acf.set_index("L"), "Время", "Значение автокорреляции", "red"
    )

    st.divider()
    st.markdown("#### График Ковариационной функции")
    cf = analysis.acf(shift_noise_data, "Ковариационная функция")
    analysis_utils.plot_autocorrelation(
        cf.set_index("L"), "Время", "Значение ковариации", "red"
    )

    st.divider()
    cross_correlation = analysis.ccf(shift_noise_data, data_cross)

    st.markdown("#### График кроскорреляции")
    analysis_utils.plot_cross_correlation(
        cross_correlation.set_index("L"), "Время", "Значение кроскорреляции", "red"
    )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2023 StepKonst. Все права защищены.")


if __name__ == "__main__":
    main()
