import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Business Insights",
    page_icon="📊",
    layout="wide"
)

# ==========================
# Load Data
# ==========================

@st.cache_data
def load_data():
    return pd.read_csv("data/Luxury_Products_Apparel_Data.csv")

df = load_data()

st.title("📊 Business Insights Dashboard")
st.markdown("Deep analytical insights from luxury fashion product data.")

# ==========================
# KPI Section
# ==========================

total_products = len(df)
total_categories = df["Category"].nunique()
total_subcategories = df["SubCategory"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Products", total_products)

with col2:
    st.metric("Categories", total_categories)

with col3:
    st.metric("Sub Categories", total_subcategories)

st.divider()

# ==========================
# Category Distribution
# ==========================

st.subheader("🏷️ Category Distribution")

category_counts = (
    df["Category"]
    .value_counts()
    .reset_index()
)

category_counts.columns = ["Category", "Count"]

fig = px.bar(
    category_counts,
    x="Category",
    y="Count",
    text="Count",
    title="Products per Category"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Pie Chart
# ==========================

st.subheader("🥧 Category Share")

fig2 = px.pie(
    category_counts,
    values="Count",
    names="Category",
    hole=0.5
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================
# Top Categories
# ==========================

st.subheader("🔥 Top Performing Categories")

top5 = category_counts.head(5)

fig3 = px.funnel(
    top5,
    x="Count",
    y="Category"
)

st.plotly_chart(fig3, use_container_width=True)

# ==========================
# Subcategory Analysis
# ==========================

st.subheader("📈 SubCategory Analysis")

subcat = (
    df["SubCategory"]
    .value_counts()
    .head(15)
    .reset_index()
)

subcat.columns = ["SubCategory", "Count"]

fig4 = px.bar(
    subcat,
    x="Count",
    y="SubCategory",
    orientation="h",
    title="Top 15 SubCategories"
)

st.plotly_chart(fig4, use_container_width=True)

# ==========================
# Description Analysis
# ==========================

st.subheader("📝 Description Intelligence")

df["Description_Length"] = (
    df["Description"]
    .fillna("")
    .apply(len)
)

avg_len = int(df["Description_Length"].mean())
max_len = int(df["Description_Length"].max())
min_len = int(df["Description_Length"].min())

col1, col2, col3 = st.columns(3)

col1.metric("Average Length", avg_len)
col2.metric("Maximum Length", max_len)
col3.metric("Minimum Length", min_len)

fig5 = px.histogram(
    df,
    x="Description_Length",
    nbins=40,
    title="Description Length Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# ==========================
# AI Generated Insights
# ==========================

st.subheader("🤖 AI Generated Insights")

top_category = category_counts.iloc[0]["Category"]
top_count = category_counts.iloc[0]["Count"]

least_category = category_counts.iloc[-1]["Category"]

st.success(
    f"""
    Most dominant category is **{top_category}**
    with **{top_count} products**.
    """
)

st.info(
    f"""
    Dataset contains **{total_categories} categories**
    and **{total_subcategories} subcategories**.
    """
)

st.warning(
    f"""
    Category **{least_category}**
    has the lowest representation and may
    indicate a niche luxury segment.
    """
)

# ==========================
# Correlation Style Insight
# ==========================

st.subheader("📌 Executive Summary")

summary = f"""
### Key Findings

✔ Dataset contains **{total_products} luxury products**

✔ Products are distributed across
**{total_categories} categories**

✔ Most represented category:
**{top_category}**

✔ Average description length:
**{avg_len} characters**

✔ Rich product descriptions suggest
strong focus on premium branding.

✔ Product concentration indicates
strong demand in dominant luxury segments.

### Recommendation

Businesses should focus inventory,
marketing campaigns and recommendation
systems around the top-performing categories
while exploring growth opportunities
in underrepresented segments.
"""

st.markdown(summary)

# ==========================
# Download Report
# ==========================

st.download_button(
    label="📥 Download Dataset",
    data=df.to_csv(index=False),
    file_name="Luxury_Fashion_Analytics.csv",
    mime="text/csv"
)
