import streamlit as st
from st_pages import add_page_title, show_pages_from_config

add_page_title()

show_pages_from_config()

st.markdown("## Каждая лабораторная работа вносит свой вклад в развитие приложения.")
st.write(
    """Этот проект представляет собой собрание лабораторных работ, выполненных в 
    рамках курса "Экспериментальные методы обработки данных"."""
)
