import pandas as pd
import streamlit as st

from model import Model


def main():
    st.title("Визуализация данных трендов")
    
    st.sidebar.title("📈 Тренды")

    model = Model()

    trend_type = st.sidebar.selectbox(
        "Выберите тип тренда", [
            "Линейно восходящий тренд",
            "Линейно нисходящий тренд",
            "Нелинейно восходящий тренд",
            "Нелинейно нисходящий тренд"
        ]
    )
    a_value = st.slider(
        "Выберите значение \"a\"", min_value=0.01, max_value=1.0, step=0.01, value=0.1
    )
    b_value = st.slider(
        "Выберите значение \"b\"", min_value=0.01, max_value=1.0, step=0.01, value=0.1
    )
    N_value = st.slider(
        "Выберите значение \"N\"", min_value=1, max_value=1000, step=1, value=100
    )

    t, data = model.trend(trend_type, a_value, b_value, N_value)

    st.subheader("Данные о тенденциях:")
    st.line_chart(data)

    st.sidebar.subheader("Таблица данных тренда:")
    st.sidebar.dataframe(pd.DataFrame({"Время": t, "Data": data}), width=300)


if __name__ == "__main__":
    main()
