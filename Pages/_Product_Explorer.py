import streamlit as st
import pandas as pd

df = pd.read_csv("data/Luxury_Products_Apparel_Data.csv")

st.title("🔍 Product Explorer")

search = st.text_input("Search Product")

filtered = df[
    df["ProductName"].str.contains(
        search,
        case=False,
        na=False
    )
]

st.dataframe(filtered)
