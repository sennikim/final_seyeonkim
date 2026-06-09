import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path

# Always resolve data paths relative to this file, not the working directory
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Color Trend Dashboard",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=Playfair+Display:wght@700&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  .main { background-color: #FAF9F7; }

  /* Hero header */
  .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    color: #1a1a1a;
    line-height: 1.1;
    margin-bottom: 0.2rem;
  }
  .hero-sub {
    font-size: 1rem;
    color: #6b6b6b;
    font-weight: 300;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }

  /* KPI cards */
  .kpi-card {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 5px solid;
    height: 100%;
  }
  .kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a1a;
  }
  .kpi-label {
    font-size: 0.78rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
  }
  .kpi-delta {
    font-size: 0.82rem;
    color: #4caf50;
    font-weight: 500;
    margin-top: 0.3rem;
  }

  /* Color swatch badges */
  .swatch-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 0.5rem; }
  .swatch {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    border: 2px solid white;
    cursor: pointer;
  }
  .swatch-label {
    font-size: 0.7rem;
    color: #666;
    text-align: center;
    margin-top: 3px;
    max-width: 60px;
  }
  .swatch-item { display: flex; flex-direction: column; align-items: center; }

  /* Section headers */
  .section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #1a1a1a;
    margin-bottom: 0.2rem;
  }
  .section-divider {
    height: 3px;
    background: linear-gradient(90deg, #E2583E, #BB2649, #5F4B8B, #45B5AA);
    border-radius: 2px;
    margin-bottom: 1.2rem;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background-color: #1a1a1a !important;
  }
  [data-testid="stSidebar"] * {
    color: #f0ede8 !important;
  }
  [data-testid="stSidebar"] .stSlider > div { color: #f0ede8 !important; }

  /* Pantone card */
  .pantone-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    text-align: center;
  }
  .pantone-swatch { height: 160px; }
  .pantone-info { padding: 1rem; }
  .pantone-year { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 0.1em; }
  .pantone-name { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #1a1a1a; margin-top: 0.2rem; }
  .pantone-hex  { font-size: 0.8rem; color: #aaa; margin-top: 0.1rem; font-family: monospace; }

  /* Tooltip box */
  .info-box {
    background: #f4f0ff;
    border-left: 4px solid #5F4B8B;
    padding: 0.8rem 1rem;
    border-radius: 0 10px 10px 0;
    font-size: 0.88rem;
    color: #333;
    margin-bottom: 1rem;
  }
</style>
""", unsafe_allow_html=True)


# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    pantone  = pd.read_csv(DATA_DIR / "pantone_color_of_year.csv")
    fashion  = pd.read_csv(DATA_DIR / "fashion_color_trends.csv")
    social   = pd.read_csv(DATA_DIR / "social_media_color_trends.csv")
    film     = pd.read_csv(DATA_DIR / "film_color_palettes.csv")
    pop      = pd.read_csv(DATA_DIR / "color_family_popularity.csv")
    return pantone, fashion, social, film, pop

pantone_df, fashion_df, social_df, film_df, pop_df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎨 Color Trend Dashboard")
    st.markdown("---")

    st.markdown("### 🗓️ Year Range")
    year_range = st.slider(
        "Select Years",
        min_value=2010, max_value=2024,
        value=(2015, 2024),
        label_visibility="collapsed"
    )

    st.markdown("### 🏭 Industries")
    industries_all = pop_df["industry"].unique().tolist()
    selected_industries = st.multiselect(
        "Select Industries",
        options=industries_all,
        default=industries_all[:3],
        label_visibility="collapsed"
    )

    st.markdown("### 🎬 Film Genres")
    genres_all = film_df["genre"].unique().tolist()
    selected_genres = st.multiselect(
        "Select Genres",
        options=genres_all,
        default=genres_all[:4],
        label_visibility="collapsed"
    )

    st.markdown("### 🌐 Social Platforms")
    platforms_all = social_df["platform"].unique().tolist()
    selected_platforms = st.multiselect(
        "Select Platforms",
        options=platforms_all,
        default=platforms_all,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<small style='color:#888'>Data sources: Pantone, simulated industry trend data</small>", unsafe_allow_html=True)


# ── Filter Data ───────────────────────────────────────────────────────────────
y1, y2 = year_range
pop_filtered    = pop_df[(pop_df["year"].between(y1, y2)) & (pop_df["industry"].isin(selected_industries))]
film_filtered   = film_df[(film_df["year"].between(y1, y2)) & (film_df["genre"].isin(selected_genres))]
social_filtered = social_df[(social_df["year"].between(y1, y2)) & (social_df["platform"].isin(selected_platforms))]
fashion_filtered = fashion_df[fashion_df["year"].between(y1, y2)]
pantone_filtered = pantone_df[pantone_df["year"].between(y1, y2)]


# ═══════════════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding: 1.5rem 0 0.5rem 0;">
  <div class="hero-sub">Interactive Visual Analytics</div>
  <div class="hero-title">Color Trend Dashboard</div>
  <div style="margin-top:0.4rem; color:#888; font-size:0.95rem;">
    Analyzing visual color movements across Fashion, Film, Social Media &amp; Design Industries
  </div>
</div>
""", unsafe_allow_html=True)

# Color bar decoration
hex_bar = ["#BB2649","#E2583E","#EFC050","#88B04B","#45B5AA","#5A5B9F","#5F4B8B","#D94F70","#FFBE98","#9BB7D4"]
bar_html = '<div style="display:flex;gap:4px;margin:0.8rem 0 1.5rem 0;">'
for h in hex_bar:
    bar_html += f'<div style="flex:1;height:8px;border-radius:4px;background:{h};"></div>'
bar_html += '</div>'
st.markdown(bar_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ═══════════════════════════════════════════════════════════════════════════════
k1, k2, k3, k4 = st.columns(4)

top_family = pop_filtered.groupby("color_family")["popularity_index"].mean().idxmax() if not pop_filtered.empty else "—"
avg_pop    = round(pop_filtered["popularity_index"].mean(), 1) if not pop_filtered.empty else 0
pantone_count = len(pantone_filtered["year"].unique())
top_film_mood = film_filtered["mood"].value_counts().index[0] if not film_filtered.empty else "—"

kpi_data = [
    (k1, "#BB2649", "🏆 Trending Color Family", top_family, f"{y1}–{y2} average"),
    (k2, "#5F4B8B", "📊 Avg Popularity Index", f"{avg_pop}", "across selected industries"),
    (k3, "#45B5AA", "🎨 Pantone Years Covered", str(pantone_count), "Color of the Year picks"),
    (k4, "#EFC050", "🎬 Dominant Film Mood", top_film_mood, "most common palette mood"),
]

for col, border, label, val, sub in kpi_data:
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color:{border}">
          <div class="kpi-value">{val}</div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-delta">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌈 Color Families",
    "👗 Fashion",
    "🎬 Film",
    "📱 Social Media",
    "🎨 Pantone Archive"
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · COLOR FAMILIES
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">Color Family Popularity Over Time</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if pop_filtered.empty:
        st.warning("No data for selected filters.")
    else:
        # Line chart
        line_data = pop_filtered.groupby(["year","color_family"])["popularity_index"].mean().reset_index()

        color_palette = {
            "Red":"#E2583E","Blue":"#9BB7D4","Green":"#88B04B",
            "Yellow":"#EFC050","Purple":"#5F4B8B","Pink":"#D94F70",
            "Orange":"#FF8C00","Neutral":"#C4A4A4"
        }

        fig_line = px.line(
            line_data, x="year", y="popularity_index", color="color_family",
            color_discrete_map=color_palette,
            markers=True,
            labels={"popularity_index":"Popularity Index","year":"Year","color_family":"Color Family"},
            title=""
        )
        fig_line.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            xaxis=dict(showgrid=False, tickformat="d"),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f0", range=[0,110]),
            height=420,
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Heatmap
        st.markdown('<div class="section-header" style="font-size:1.2rem">Industry × Color Family Heatmap</div>', unsafe_allow_html=True)
        heat_data = pop_filtered.groupby(["industry","color_family"])["popularity_index"].mean().reset_index()
        heat_pivot = heat_data.pivot(index="color_family", columns="industry", values="popularity_index").fillna(0)

        fig_heat = px.imshow(
            heat_pivot,
            color_continuous_scale=["#FAF9F7","#FFBE98","#E2583E","#BB2649","#5F4B8B"],
            aspect="auto",
            labels=dict(color="Popularity"),
        )
        fig_heat.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans",
            height=360,
            coloraxis_colorbar=dict(title="Index"),
        )
        st.plotly_chart(fig_heat, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · FASHION
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">Fashion Color Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])

    with col_a:
        # Bar: top colors by runway appearances
        top_colors = (
            fashion_filtered.groupby(["color_name","hex","color_family"])["runway_appearances"]
            .sum().reset_index()
            .sort_values("runway_appearances", ascending=False)
            .head(12)
        )
        fig_bar = px.bar(
            top_colors, x="runway_appearances", y="color_name",
            orientation="h",
            color="hex",
            color_discrete_map={h:h for h in top_colors["hex"]},
            labels={"runway_appearances":"Runway Appearances","color_name":""},
            title="Top Colors by Runway Appearances",
        )
        fig_bar.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", showlegend=False,
            height=420,
            yaxis=dict(autorange="reversed"),
            xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        # Pie: color family distribution
        fam_counts = fashion_filtered["color_family"].value_counts().reset_index()
        fam_counts.columns = ["color_family","count"]
        fam_palette = {"Blue":"#9BB7D4","Orange":"#E2583E","Green":"#88B04B",
                       "Pink":"#D94F70","Yellow":"#EFC050","Purple":"#5F4B8B",
                       "Neutral":"#C4A4A4","Red":"#BB2649"}
        fig_pie = px.pie(
            fam_counts, names="color_family", values="count",
            color="color_family", color_discrete_map=fam_palette,
            title="Color Family Distribution",
            hole=0.45,
        )
        fig_pie.update_layout(
            font_family="DM Sans", paper_bgcolor="white",
            height=420,
            legend=dict(orientation="v", x=1.05),
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Scatter: popularity vs runway
    st.markdown('<div class="section-header" style="font-size:1.2rem">Popularity vs. Runway Presence</div>', unsafe_allow_html=True)
    scatter_data = fashion_filtered.groupby(["color_name","hex","color_family"]).agg(
        popularity=("popularity_score","mean"),
        runway=("runway_appearances","sum"),
    ).reset_index()

    fig_scatter = px.scatter(
        scatter_data, x="runway", y="popularity",
        color="color_family", color_discrete_map=fam_palette,
        size="runway", hover_name="color_name",
        labels={"runway":"Runway Appearances","popularity":"Avg Popularity Score"},
    )
    fig_scatter.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="DM Sans", height=380,
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Color swatches
    st.markdown('<div class="section-header" style="font-size:1.2rem">🎨 Fashion Color Palette</div>', unsafe_allow_html=True)
    unique_colors = fashion_filtered[["color_name","hex"]].drop_duplicates().head(15)
    swatch_html = '<div class="swatch-row">'
    for _, row in unique_colors.iterrows():
        swatch_html += f'''
        <div class="swatch-item">
          <div class="swatch" style="background:{row["hex"]}" title="{row["color_name"]} {row["hex"]}"></div>
          <div class="swatch-label">{row["color_name"]}</div>
        </div>'''
    swatch_html += '</div>'
    st.markdown(swatch_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · FILM
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">Film Color Palettes</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    col_c, col_d = st.columns(2)

    with col_c:
        # Grouped bar: dominant color by genre
        genre_color = film_filtered.groupby(["genre","dominant_color","hex"]).size().reset_index(name="count")
        top_gc = genre_color.sort_values("count", ascending=False).drop_duplicates("genre")
        fig_genre = px.bar(
            top_gc, x="genre", y="count",
            color="hex",
            color_discrete_map={h:h for h in top_gc["hex"]},
            hover_data=["dominant_color"],
            title="Most Common Color per Genre",
            labels={"count":"Films","genre":"Genre"},
        )
        fig_genre.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", showlegend=False, height=380,
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig_genre, use_container_width=True)

    with col_d:
        # Pie: mood distribution
        mood_counts = film_filtered["mood"].value_counts().reset_index()
        mood_counts.columns = ["mood","count"]
        mood_palette = {
            "Mysterious":"#191970","Nostalgic":"#FFD700","Passionate":"#8B0000",
            "Futuristic":"#9B59B6","Energetic":"#FF8C00","Calm":"#B0E0E6",
            "Gritty":"#36454F","Playful":"#32CD32",
        }
        fig_mood = px.pie(
            mood_counts, names="mood", values="count",
            color="mood", color_discrete_map=mood_palette,
            title="Film Mood Distribution",
            hole=0.4,
        )
        fig_mood.update_layout(font_family="DM Sans", paper_bgcolor="white", height=380)
        fig_mood.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_mood, use_container_width=True)

    # Line: audience score by year
    score_trend = film_filtered.groupby("year")["avg_audience_score"].mean().reset_index()
    fig_score = px.area(
        score_trend, x="year", y="avg_audience_score",
        title="Average Audience Score Over Time",
        labels={"avg_audience_score":"Score (0–100)","year":"Year"},
        color_discrete_sequence=["#5F4B8B"],
    )
    fig_score.update_traces(fill='tozeroy', fillcolor='rgba(95,75,139,0.15)')
    fig_score.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="DM Sans", height=300,
        xaxis=dict(showgrid=False, tickformat="d"),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    )
    st.plotly_chart(fig_score, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 · SOCIAL MEDIA
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">Social Media Color Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    col_e, col_f = st.columns(2)

    with col_e:
        # Bar: top aesthetics by engagement
        aes_eng = social_filtered.groupby("aesthetic")["engagement_score"].mean().reset_index()
        aes_eng = aes_eng.sort_values("engagement_score", ascending=False)
        fig_aes = px.bar(
            aes_eng, x="aesthetic", y="engagement_score",
            title="Avg Engagement by Aesthetic",
            labels={"engagement_score":"Engagement Score","aesthetic":"Aesthetic"},
            color="engagement_score",
            color_continuous_scale=["#FFBE98","#E2583E","#BB2649"],
        )
        fig_aes.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", showlegend=False, height=380,
            xaxis_tickangle=-35, coloraxis_showscale=False,
        )
        st.plotly_chart(fig_aes, use_container_width=True)

    with col_f:
        # Treemap: platform x vibe
        vibe_data = social_filtered.groupby(["platform","vibe"])["posts_millions"].sum().reset_index()
        fig_tree = px.treemap(
            vibe_data, path=["platform","vibe"], values="posts_millions",
            title="Posts Volume: Platform × Vibe",
            color="posts_millions",
            color_continuous_scale=["#f4f0ff","#9B59B6","#5F4B8B"],
        )
        fig_tree.update_layout(font_family="DM Sans", paper_bgcolor="white", height=380)
        st.plotly_chart(fig_tree, use_container_width=True)

    # Line: posts over time per platform
    posts_time = social_filtered.groupby(["year","platform"])["posts_millions"].sum().reset_index()
    fig_posts = px.line(
        posts_time, x="year", y="posts_millions", color="platform",
        markers=True,
        title="Posts Volume Over Time by Platform (Millions)",
        labels={"posts_millions":"Posts (M)","year":"Year"},
    )
    fig_posts.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="DM Sans", height=340,
        xaxis=dict(showgrid=False, tickformat="d"),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        hovermode="x unified",
    )
    st.plotly_chart(fig_posts, use_container_width=True)

    # Color swatches per vibe
    st.markdown('<div class="section-header" style="font-size:1.2rem">🌐 Trending Social Media Colors</div>', unsafe_allow_html=True)
    sm_palette = social_filtered[["color_name","hex","vibe"]].drop_duplicates("color_name").sort_values("vibe")
    swatch_html2 = '<div class="swatch-row">'
    for _, row in sm_palette.iterrows():
        swatch_html2 += f'''
        <div class="swatch-item">
          <div class="swatch" style="background:{row["hex"]}" title="{row["color_name"]} ({row["vibe"]})"></div>
          <div class="swatch-label">{row["color_name"]}</div>
        </div>'''
    swatch_html2 += '</div>'
    st.markdown(swatch_html2, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 · PANTONE ARCHIVE
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-header">Pantone Color of the Year Archive</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="info-box">Pantone has selected a Color of the Year since 2000. These choices influence product design, fashion, interiors, and graphic design worldwide.</div>', unsafe_allow_html=True)

    pantone_show = pantone_df[pantone_df["year"].between(y1, y2)].sort_values("year", ascending=False)

    # Cards grid (up to 4 per row)
    cols_per_row = 4
    rows = [pantone_show.iloc[i:i+cols_per_row] for i in range(0, len(pantone_show), cols_per_row)]

    for row_df in rows:
        cols = st.columns(cols_per_row)
        for col, (_, p) in zip(cols, row_df.iterrows()):
            with col:
                st.markdown(f"""
                <div class="pantone-card">
                  <div class="pantone-swatch" style="background:{p['hex']}"></div>
                  <div class="pantone-info">
                    <div class="pantone-year">{int(p['year'])}</div>
                    <div class="pantone-name">{p['color_name']}</div>
                    <div class="pantone-hex">{p['hex']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # RGB breakdown bubble chart
    st.markdown('<div class="section-header" style="font-size:1.2rem">RGB Composition of Pantone Colors</div>', unsafe_allow_html=True)
    fig_rgb = go.Figure()
    channels = [("Red","rgb_r","#E2583E"),("Green","rgb_g","#88B04B"),("Blue","rgb_b","#9BB7D4")]
    for label, col, clr in channels:
        fig_rgb.add_trace(go.Scatter(
            x=pantone_show["year"], y=pantone_show[col],
            mode="lines+markers", name=label,
            line=dict(color=clr, width=2),
            marker=dict(size=8, color=clr),
        ))
    fig_rgb.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="DM Sans", height=360,
        xaxis=dict(showgrid=False, tickformat="d", title="Year"),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", title="RGB Value (0–255)"),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig_rgb, use_container_width=True)

    # Color picker tool
    st.markdown("---")
    st.markdown('<div class="section-header" style="font-size:1.2rem">🖌️ Color Inspector Tool</div>', unsafe_allow_html=True)
    pick_col1, pick_col2 = st.columns([1, 2])

    with pick_col1:
        picked = st.color_picker("Pick any color to inspect", "#BB2649")
        r = int(picked[1:3], 16)
        g = int(picked[3:5], 16)
        b = int(picked[5:7], 16)
        brightness = round((r * 0.299 + g * 0.587 + b * 0.114) / 255 * 100, 1)
        saturation_proxy = round((max(r,g,b) - min(r,g,b)) / 255 * 100, 1)
        text_color = "#fff" if brightness < 50 else "#1a1a1a"

    with pick_col2:
        st.markdown(f"""
        <div style="background:{picked};border-radius:16px;padding:2rem;color:{text_color};min-height:140px;">
          <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;">{picked.upper()}</div>
          <div style="margin-top:0.5rem;opacity:0.85;">RGB: {r}, {g}, {b}</div>
          <div style="opacity:0.75;font-size:0.88rem;">Brightness: {brightness}% · Saturation proxy: {saturation_proxy}%</div>
        </div>
        """, unsafe_allow_html=True)

        # Find closest Pantone
        pantone_df["dist"] = pantone_df.apply(
            lambda row: ((row["rgb_r"]-r)**2 + (row["rgb_g"]-g)**2 + (row["rgb_b"]-b)**2)**0.5, axis=1
        )
        closest = pantone_df.loc[pantone_df["dist"].idxmin()]
        st.markdown(f"""
        <div style="margin-top:0.8rem;background:#f9f9f9;border-radius:10px;padding:0.8rem 1rem;display:flex;align-items:center;gap:1rem;">
          <div style="width:40px;height:40px;border-radius:50%;background:{closest['hex']};flex-shrink:0;box-shadow:0 2px 6px rgba(0,0,0,.15);"></div>
          <div>
            <div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:.08em;">Closest Pantone</div>
            <div style="font-weight:600;color:#1a1a1a;">{closest['color_name']} ({int(closest['year'])})</div>
            <div style="font-size:0.8rem;color:#aaa;font-family:monospace;">{closest['hex']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#bbb;font-size:0.8rem;padding:0.5rem 0 1.5rem 0;">
  Color Trend Dashboard · Built with Streamlit & Plotly ·
  Data: Pantone Color Institute (historical) + Simulated industry trend data
</div>
""", unsafe_allow_html=True)
