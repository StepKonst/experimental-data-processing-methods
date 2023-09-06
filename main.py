import pandas as pd
import streamlit as st

from model import Model


def main():
    st.title("Trend Data Visualization")

    model = Model()

    trend_type = st.selectbox(
        "Type", ["Linear Up", "Linear Down", "Nonlinear Up", "Nonlinear Down"]
    )
    a_value = st.slider(
        "Enter 'a' value", min_value=0.01, max_value=1.0, step=0.01, value=0.1
    )
    b_value = st.slider(
        "Enter 'b' value", min_value=0.01, max_value=1.0, step=0.01, value=0.1
    )
    N_value = st.slider(
        "Enter 'N' value", min_value=1, max_value=1000, step=1, value=100
    )

    t, data = model.trend(trend_type, a_value, b_value, N_value)

    st.subheader("Trend Data:")
    st.line_chart(data)

    st.subheader("Trend Data Table:")
    st.write(pd.DataFrame({"Time": t, "Data": data}))


if __name__ == "__main__":
    main()
