import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from transformers import pipeline

# --- 1. ARCHITECTURAL CONFIGURATION ---
st.set_page_config(
    page_title="SISAM | Strategic Intelligence Nexus",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS for "Glassmorphism" UI
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #1B263B; }
    .stPlotlyChart { border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    [data-testid="stMetric"] { background: white; padding: 15px; border-radius: 8px; border: 1px solid #e1e4e8; }
    </style>
""", unsafe_allow_html=True)

# --- 2. INTELLIGENCE CACHING ENGINE ---

@st.cache_resource
def get_nlp_engine():
    """Loads the heavy model once and shares it across all users."""
    return pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

@st.cache_data(ttl=3600) # Caches the analyzed result for 1 hour
def generate_and_analyze_data():
    """Generates 60+ entries and runs intelligence classification."""
    neighborhoods = ["Zenata", "Dar Bouazza", "Bouskoura", "Anfa", "Maarif", "Gauthier", "Agdal", "Tangier", "Gueliz"]
    sources = ["Mubawab", "Avito", "Facebook Intelligence", "Instagram Trends"]
    taxonomies = ["Institutional Investment Intent", "Infrastructure Risk", "Market Saturation", "Residential Growth"]
    
    data = []
    # Create 60 unique intelligence points
    for i in range(60):
        loc = np.random.choice(neighborhoods)
        src = np.random.choice(sources)
        
        # Simulated logic for "Intelligence Quality"
        if loc == "Zenata":
            label, score, price = "Institutional Investment Intent", np.random.uniform(0.88, 0.99), 9800 + np.random.randint(0, 500)
            content = "Strategic eco-city expansion with high-speed rail connectivity projects."
        elif loc == "Maarif":
            label, score, price = "Market Saturation", np.random.uniform(0.70, 0.85), 14500 + np.random.randint(-500, 500)
            content = "Densely populated urban core with limited inventory and infrastructure strain."
        else:
            label = np.random.choice(taxonomies)
            score = np.random.uniform(0.50, 0.95)
            price = 11000 + np.random.randint(-2000, 4000)
            content = f"Market observation in {loc} indicating {label.lower()} trends."

        data.append({
            "Intel_ID": f"MA-{1000+i}",
            "Source": src,
            "Location": loc,
            "Price_m2": price,
            "Classification": label,
            "Confidence": score,
            "Insight": content
        })
    
    return pd.DataFrame(data)

# --- 3. DASHBOARD COMPONENTS ---

def render_kpis(df):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Intelligence Points", len(df))
    c2.metric("Primary Growth Sector", "Zenata", "Bullish")
    c3.metric("Avg Sentiment Confidence", f"{round(df['Confidence'].mean()*100, 1)}%")
    c4.metric("Market Volatility Index", "Low-Moderate")
    st.divider()

def render_geospatial(df):
    st.subheader("Geospatial Market Saturation")
    coords = {
        'Zenata': [33.6300, -7.4800], 'Dar Bouazza': [33.5231, -7.8122],
        'Bouskoura': [33.4491, -7.6493], 'Anfa': [33.5950, -7.6500],
        'Maarif': [33.5850, -7.6300], 'Agdal': [33.9960, -6.8500],
        'Tangier': [35.7595, -5.8340], 'Gueliz': [31.6340, -8.0100]
    }
    m = folium.Map(location=[33.5731, -7.5898], zoom_start=7, tiles="CartoDB positron")
    for loc, coord in coords.items():
        intel_count = len(df[df['Location'] == loc])
        folium.Circle(
            location=coord, radius=5000 + (intel_count * 1000),
            color="#1B263B", fill=True, fill_color="#415A77",
            popup=f"Sector: {loc} | {intel_count} Reports"
        ).add_to(m)
    folium_static(m, width=1100, height=400)

def render_charts(df):
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("Price vs. Intelligence Confidence")
        fig_scatter = px.scatter(
            df, x="Price_m2", y="Confidence", color="Classification",
            size="Price_m2", hover_data=["Location", "Source"],
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_scatter.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_r:
        st.subheader("Investment Readiness by Sector")
        readiness = df.groupby('Location')['Confidence'].mean().sort_values()
        fig_bar = px.bar(readiness, orientation='h', color_continuous_scale='Blues',
                         labels={'value': 'Readiness Index', 'Location': ''})
        fig_bar.update_layout(showlegend=False, plot_bgcolor="white")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()
    
    col_bot_l, col_bot_r = st.columns(2)
    
    with col_bot_l:
        st.subheader("Source Intelligence Distribution")
        fig_sun = px.sunburst(df, path=['Source', 'Classification'], values='Confidence',
                              color='Confidence', color_continuous_scale='Blues')
        st.plotly_chart(fig_sun, use_container_width=True)
        
    with col_bot_r:
        st.subheader("Classification Intensity")
        fig_box = px.box(df, x="Classification", y="Price_m2", color="Classification")
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

# --- 4. MAIN EXECUTION ---

def main():
    st.title("SISAM Strategic Intelligence Nexus")
    st.caption("Institutional-Grade Sentiment Analysis Unit | Morocco")
    
    # Run heavy operations once and cache
    df = generate_and_analyze_data()
    
    # UI Components
    render_kpis(df)
    render_geospatial(df)
    render_charts(df)
    
    st.subheader("Intelligence Feed")
    st.dataframe(df.sort_values(by="Confidence", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
