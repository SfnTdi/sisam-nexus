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
    st.info("SISAM V4.4: Strategic Intelligence and Sentiment Analysis for Groupe Addoha.")

# Dynamic CSS based on theme selection
if ui_theme == "Executive Dark":
    chart_template = "plotly_dark"
    bg_color = "#0e1117"
    text_color = "#FFFFFF"
    accent_color = "#f39c12" # Addoha Sun Gold
    # Colors for Scatter Plot
    color_map = {
        "High Investment Intent": "#2E86C1", 
        "Infrastructure Risk": "#E74C3C",    
        "Market Saturation": "#7F8C8D",     
        "Luxury Growth Sector": "#F39C12"   
    }
else:
    chart_template = "plotly_white"
    bg_color = "#F8F9FA"
    text_color = "#1B263B"
    accent_color = "#E67E22"
    # Colors for Scatter Plot
    color_map = {
        "High Investment Intent": "#21618C", 
        "Infrastructure Risk": "#C0392B",    
        "Market Saturation": "#707B7C",     
        "Luxury Growth Sector": "#D68910"
    }

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
            # Ensure your logo file is named exactly 'logo.png' in your GitHub/folder
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
    # Analyzing 65 Intelligence Points
    for i in range(65):
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

    # GRAPHS
    c_left, c_right = st.columns(2)
    
    with c_left:
        # Investment Potential Scatter (Fixed Dark Mode & Corporate Colors)
        st.subheader("Investment Potential vs. Value")
        fig_scatter = px.scatter(
            df, x="Price_m2", y="Sentiment_Score", 
            color="Classification", 
            color_discrete_map=color_map,
            template=chart_template, 
            size="Sentiment_Score", 
            hover_data=["Location"]
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color=text_color
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c_right:
        # Readiness Index (Fixed Color: Light Blue Gradient)
        st.subheader("Readiness Index by Sector")
        readiness = df.groupby('Location')['Sentiment_Score'].mean().sort_values()
        fig_bar = px.bar(
            readiness, 
            orientation='h', 
            template=chart_template, 
            color=readiness.values,
            color_continuous_scale=['#D1E8FF', '#3399FF', '#0052A3'] # Light Blue to Deep Blue
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color=text_color, 
            showlegend=False,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # ADDOHA SPECIFIC INSIGHTS
    c_sun, c_table = st.columns([1, 1])
    
    with c_sun:
        st.subheader("Source Sentiment Sunburst")
        fig_sun = px.sunburst(
            df, path=['Source', 'Classification'], values='Sentiment_Score', 
            template=chart_template, color='Sentiment_Score', 
            color_continuous_scale='YlOrBr'
        )
        fig_sun.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color=text_color)
        st.plotly_chart(fig_sun, use_container_width=True)

    with c_table:
        st.subheader("Institutional Feed")
        st.dataframe(
            df[['Intel_ID', 'Location', 'Classification', 'Sentiment_Score']].sort_values(by="Sentiment_Score", ascending=False), 
            use_container_width=True,
            height=400
        )

# --- 5. MAIN EXECUTION ---
if __name__ == "__main__":
    render_header()
    data = get_strategic_data()
    render_analytics(data)
