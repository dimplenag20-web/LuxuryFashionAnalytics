import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Luxury Fashion Analytics",
    page_icon="👗",
    layout="wide"
)

@st.cache_data
def load_data():

    st.write("Current Directory:", os.getcwd())

    st.write("Root Files:", os.listdir("."))

    if os.path.exists("data"):
        st.write("Data Folder Files:", os.listdir("data"))
    else:
        st.error("data folder not found")

    return pd.read_csv("data/Luxury_Products_Apparel_Data.csv")

df = load_data()

st.title("💎 Luxury Fashion Analytics Dashboard")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Products", len(df))
col2.metric("Categories", df["Category"].nunique())
col3.metric("SubCategories", df["SubCategory"].nunique())
col4.metric("Descriptions", df["Description"].notna().sum())

st.divider()

category_counts = df["Category"].value_counts()

fig = px.bar(
    category_counts,
    x=category_counts.index,
    y=category_counts.values,
    title="Category Distribution"
)

st.plotly_chart(fig,use_container_width=True)
