import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re

st.set_page_config(page_title="AI Analytics", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/Luxury_Products_Apparel_Data.csv")

df = load_data()

st.title("🤖 AI Analytics Dashboard")

# ===========================
# Dataset Overview
# ===========================

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Products", len(df))
col2.metric("Categories", df["Category"].nunique())
col3.metric("Sub Categories", df["SubCategory"].nunique())

# ===========================
# Category Analysis
# ===========================

st.subheader("📊 Category Intelligence")

category_count = df["Category"].value_counts()

fig = px.bar(
    x=category_count.index,
    y=category_count.values,
    labels={"x":"Category","y":"Products"},
    title="Products per Category"
)

st.plotly_chart(fig, use_container_width=True)

top_category = category_count.idxmax()

st.success(
    f"AI Insight: '{top_category}' dominates the dataset with "
    f"{category_count.max()} products."
)

# ===========================
# NLP Analysis
# ===========================

st.subheader("🧠 NLP Keyword Extraction")

text_data = " ".join(df["Description"].fillna(""))

text_data = re.sub(r'[^a-zA-Z ]', '', text_data)

vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=20
)

X = vectorizer.fit_transform([text_data])

keywords = pd.DataFrame({
    "Keyword": vectorizer.get_feature_names_out(),
    "Importance": X.toarray()[0]
})

keywords = keywords.sort_values(
    "Importance",
    ascending=False
)

st.dataframe(keywords)

# ===========================
# AI Generated Insights
# ===========================

st.subheader("🔍 AI Generated Business Insights")

insights = []

insights.append(
    f"Dataset contains {len(df)} luxury products."
)

insights.append(
    f"Top performing category is '{top_category}'."
)

insights.append(
    f"There are {df['SubCategory'].nunique()} distinct subcategories."
)

most_common_keyword = keywords.iloc[0]["Keyword"]

insights.append(
    f"Most influential product keyword is '{most_common_keyword}'."
)

for item in insights:
    st.info(item)

# ===========================
# Product Recommendation AI
# ===========================

st.subheader("🎯 Smart Product Finder")

selected_category = st.selectbox(
    "Choose Category",
    sorted(df["Category"].unique())
)

recommended = df[
    df["Category"] == selected_category
].sample(
    min(5, len(df[df["Category"] == selected_category]))
)

st.write("Recommended Products")

st.dataframe(
    recommended[
        ["ProductName", "SubCategory"]
    ]
)

# ===========================
# Description Length Analysis
# ===========================

st.subheader("📈 Product Description Intelligence")

df["Description_Length"] = (
    df["Description"]
    .fillna("")
    .apply(len)
)

fig2 = px.histogram(
    df,
    x="Description_Length",
    nbins=30,
    title="Description Length Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

avg_length = int(df["Description_Length"].mean())

st.success(
    f"AI Insight: Average description length is "
    f"{avg_length} characters."
)

# ===========================
# Executive Summary
# ===========================

st.subheader("📋 Executive Summary")

st.markdown(f"""
### AI Summary

- Total Products: **{len(df)}**
- Categories: **{df['Category'].nunique()}**
- SubCategories: **{df['SubCategory'].nunique()}**
- Dominant Category: **{top_category}**
- Top Keyword: **{most_common_keyword}**

### Recommendation

Focus future luxury product expansion around
**{top_category}** since it has the highest representation
within the dataset.
""")
