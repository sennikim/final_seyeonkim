import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Color Trend Dashboard",
    page_icon="🎨",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    pantone = pd.read_csv("pantone_colors.csv")
    fashion = pd.read_csv("fashion_color_trends.csv")
    social = pd.read_csv("social_media_colors.csv")

    return pantone, fashion, social

pantone_df, fashion_df, social_df = load_data()

# -----------------------------
# Standardize Columns
# -----------------------------
fashion_df.columns = [c.strip() for c in fashion_df.columns]
social_df.columns = [c.strip() for c in social_df.columns]
pantone_df.columns = [c.strip() for c in pantone_df.columns]

combined_df = pd.concat(
    [fashion_df, social_df],
    ignore_index=True
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🎨 Filters")

years = sorted(combined_df["Year"].unique())

selected_years = st.sidebar.multiselect(
    "Select Years",
    years,
    default=years
)

industries = combined_df["Industry"].unique()

selected_industries = st.sidebar.multiselect(
    "Select Industries",
    industries,
    default=industries
)

filtered = combined_df[
    (combined_df["Year"].isin(selected_years))
    &
    (combined_df["Industry"].isin(selected_industries))
]

# -----------------------------
# Header
# -----------------------------
st.title("🎨 Color Trend Dashboard")

st.markdown("""
Explore color trends across:

- Pantone Color of the Year
- Fashion Industry
- Social Media Trends
""")

# -----------------------------
# KPI Cards
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Pantone Years",
    pantone_df["Year"].nunique()
)

c2.metric(
    "Industries",
    combined_df["Industry"].nunique()
)

c3.metric(
    "Colors",
    combined_df["Color"].nunique()
)

c4.metric(
    "Records",
    len(combined_df)
)

st.divider()

# -----------------------------
# Pantone Section
# -----------------------------
st.header("🌈 Pantone Color of the Year")

st.dataframe(
    pantone_df,
    use_container_width=True
)

# -----------------------------
# Trend Line
# -----------------------------
st.header("📈 Color Popularity Trend")

fig_line = px.line(
    filtered,
    x="Year",
    y="Popularity",
    color="Color",
    markers=True
)

fig_line.update_layout(
    height=500
)

st.plotly_chart(
    fig_line,
    use_container_width=True
)

# -----------------------------
# Pie Chart
# -----------------------------
st.header("🥧 Color Distribution")

pie_df = (
    filtered
    .groupby("Color")["Popularity"]
    .sum()
    .reset_index()
)

fig_pie = px.pie(
    pie_df,
    names="Color",
    values="Popularity",
    hole=0.4
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

# -----------------------------
# Industry Comparison
# -----------------------------
st.header("📊 Industry Comparison")

bar_df = (
    filtered
    .groupby(
        ["Industry", "Color"]
    )["Popularity"]
    .mean()
    .reset_index()
)

fig_bar = px.bar(
    bar_df,
    x="Color",
    y="Popularity",
    color="Industry",
    barmode="group"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# -----------------------------
# Top Colors
# -----------------------------
st.header("🔥 Top Trending Colors")

top_colors = (
    filtered
    .groupby("Color")["Popularity"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(
    top_colors,
    use_container_width=True
)

# -----------------------------
# Color Picker
# -----------------------------
st.header("🎨 Color Picker")

picked = st.color_picker(
    "Choose a color",
    "#FFBE98"
)

st.markdown(
    f"""
    <div
    style="
    background:{picked};
    height:120px;
    border-radius:15px;
    margin-bottom:10px;
    ">
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Selected Color:", picked)

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Color Trend Dashboard | Streamlit + Plotly + Pandas"
)
