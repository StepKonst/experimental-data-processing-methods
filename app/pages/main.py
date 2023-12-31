import streamlit as st
from st_pages import add_page_title, show_pages_from_config

add_page_title()

show_pages_from_config()

st.markdown("## Домашняя страница")
st.write(
    """Приложение по предмету "Экспериментальные методы обработки данных" - это интеллектуальное решение, 
    специально разработанное для удобной и эффективной обработки и анализа данных. С помощью 
    этого приложения вы сможете легко моделировать и анализировать данные, строить графики и выполнять различные 
    виды обработки. Классы Model, Analysis и Processing в нашем приложении обеспечивают широкий спектр функциональности 
    и гибкость в работе с данными. Будь то создание сложных моделей, проведение статистического анализа или применение 
    различных алгоритмов обработки данных, наше приложение поможет вам в достижении ваших целей и 
    получении ценных инсайтов из ваших экспериментальных данных."""
)

github_link = "https://github.com/StepKonst/experimental-data-processing-methods"
st.markdown(f"[GitHub проекта]({github_link})")
