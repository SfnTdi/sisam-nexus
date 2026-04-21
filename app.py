import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from PIL import Image

# --- 1. THEME & HEADER CONFIGURATION ---
st.set_page_config(
    page_title="SISAM | Groupe Addoha Intelligence",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for Theme Control
with st.sidebar:
    st.header("Nexus Control Center")
    ui_theme = st.selectbox("Dashboard Theme", ["Executive Dark", "Institutional Light"])
    st.divider()
    st.info("SISAM V4.0: Adaptive Intelligence for Groupe Addoha Strategic Planning.")

# Dynamic CSS based on theme selection
if ui_theme == "Executive Dark":
    chart_template = "plotly_dark"
    bg_color = "#0e1117"
    text_color = "#FFFFFF"
    accent_color = "#f39c12" # Addoha Sun Gold
else:
    chart_template = "plotly_white"
    bg_color = "#F8F9FA"
    text_color = "#1B263B"
    accent_color = "#E67E22"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    [data-testid="stMetric"] {{ background: rgba(255,255,255,0.05); border: 1px solid #444; border-radius: 10px; }}
    h1, h2, h3 {{ color: {accent_color} !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER & LOGO ---
def render_header():
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        try:
            logo = Image.open("logo.png")
            st.image(logo, use_container_width=True)
        except:
            st.warning("Logo file 'logo.png' not found. Please upload to root directory.")
    
    st.markdown("<h1 style='text-align: center;'>SISAM STRATEGIC INTELLIGENCE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; opacity: 0.8;'>Strategic Intelligence and Sentiment Analysis Module</p>", unsafe_allow_html=True)
    st.divider()

# --- 3. DATA ENGINE (PERSISTENT CACHED DATA) ---
@st.cache_data
def get_strategic_data():
    neighborhoods = ["Zenata", "Dar Bouazza", "Bouskoura", "Anfa", "Maarif", "Rabat Agdal", "Tangier", "Marrakech"]
    sources = ["Mubawab", "Avito", "FB Real Estate", "IG Trends"]
    taxonomies = ["High Investment Intent", "Infrastructure Risk", "Market Saturation", "Luxury Growth Sector"]
    
    data = []
    for i in range(60):
        loc = np.random.choice(neighborhoods)
        price = 11000 + np.random.randint(-3000, 6000)
        confidence = np.random.uniform(0.60, 0.98)
        label = np.random.choice(taxonomies)
        
        data.append({
            "Intel_ID": f"AD-{2000+i}",
            "Source": np.random.choice(sources),
            "Location": loc,
            "Price_m2": price,
            "Classification": label,
            "Sentiment_Score": confidence,
            "Summary": f"Strategic analysis for {loc} indicates {label.lower()}."
        })
    return pd.DataFrame(data)

# --- 4. ANALYTICS COMPONENTS ---
def render_analytics(df):
    # KPI ROW
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Intelligence Points", len(df))
    k2.metric("Primary Growth Area", "Zenata")
    k3.metric("Analysis Confidence", f"{round(df['Sentiment_Score'].mean()*100, 1)}%")
    k4.metric("Market Sentiment", "Positive")

    st.divider()

    # GEOSPATIAL MAP
    st.subheader("Market Sentiment Heatmap")
    m = folium.Map(location=[33.5731, -7.5898], zoom_start=11, tiles="CartoDB dark_matter" if ui_theme == "Executive Dark" else "CartoDB positron")
    coords = {'Zenata': [33.63, -7.48], 'Dar Bouazza': [33.52, -7.81], 'Bouskoura': [33.44, -7.64], 'Anfa': [33.59, -7.65], 'Maarif': [33.58, -7.63]}
    
    for loc, coord in coords.items():
        score = df[df['Location'] == loc]['Sentiment_Score'].mean() if loc in df['Location'].values else 0.5
        folium.Circle(location=coord, radius=1200, color="#f39c12", fill=True, popup=f"{loc}: {round(score, 2)}").add_to(m)
    folium_static(m, width=1150)

    # GRAPHS (FIXED FOR DARK MODE)
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.subheader("Investment Potential vs. Value")
        fig_scatter = px.scatter(df, x="Price_m2", y="Sentiment_Score", color="Classification", 
                                 template=chart_template, size="Sentiment_Score", hover_data=["Location"])
        # Professional Transparency Fix
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=text_color)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c_right:
        st.subheader("Readiness Index by Sector")
        readiness = df.groupby('Location')['Sentiment_Score'].mean().sort_values()
        fig_bar = px.bar(readiness, orientation='h', template=chart_template, color_continuous_scale='YlOrBr')
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=text_color, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ADDOHA SPECIFIC INSIGHTS
    st.subheader("Source Sentiment Sunburst")
    fig_sun = px.sunburst(df, path=['Source', 'Classification'], values='Sentiment_Score', 
                          template=chart_template, color='Sentiment_Score', color_continuous_scale='YlOrBr')
    fig_sun.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color=text_color)
    st.plotly_chart(fig_sun, use_container_width=True)

    st.subheader("Institutional Feed")
    st.dataframe(df.sort_values(by="Sentiment_Score", ascending=False), use_container_width=True)

# --- 5. MAIN EXECUTION ---
if __name__ == "__main__":
    render_header()
    data = get_strategic_data()
    render_analytics(data)
