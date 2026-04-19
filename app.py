import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

# --- CACHING THE INTELLIGENCE LAYER ---
@st.cache_resource
def load_intelligence_unit():
    # Loading the model once and keeping it in memory
    classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
    return classifier

# --- DATA INGESTION ---
def get_unified_data():
    # Mock data for deployment demonstration
    data = [
        {"source": "Mubawab", "location": "Zenata", "price_mad": 950000, "content": "Eco-city development project. High appreciation potential."},
        {"source": "Avito", "location": "Dar Bouazza", "price_mad": 1200000, "content": "Waterfront property. Growing demand."},
        {"source": "Facebook", "location": "Casablanca", "price_mad": 0, "content": "Severe traffic congestion in Gauthier."},
        {"source": "Instagram", "location": "Zenata", "price_mad": 0, "content": "New retail infrastructure announced. Strategic buy signal."},
        {"source": "Facebook", "location": "Bouskoura", "price_mad": 0, "content": "Concerns regarding road maintenance."}
    ]
    return pd.DataFrame(data)

# --- DASHBOARD UI ---
def run_dashboard(df, classifier):
    st.set_page_config(page_title="SISAM Nexus", layout="wide")
    st.title("SISAM Strategic Intelligence Dashboard")
    
    # Process Sentiment
    taxonomies = ["Institutional Investment Intent", "Infrastructure Risk", "Residential Appreciation"]
    
    # Add classification only if not already processed
    if 'classification' not in df.columns:
        res = df['content'].apply(lambda x: classifier(x, taxonomies))
        df['classification'] = [x['labels'][0] for x in res]
        df['confidence'] = [x['scores'][0] for x in res]

    # Metrics
    k1, k2, k3 = st.columns(3)
    k1.metric("Intelligence Points", len(df))
    k2.metric("Top Sector", df['location'].value_counts().idxmax())
    k3.metric("System Status", "Operational")

    # Map and Chart
    c1, c2 = st.columns([2, 1])
    with c1:
        m = folium.Map(location=[33.5731, -7.5898], zoom_start=11, tiles="CartoDB positron")
        # Simplified marker logic for deployment
        folium.Marker([33.6300, -7.4800], popup="Zenata High Intent").add_to(m)
        folium_static(m)
    
    with c2:
        fig = px.pie(df, names='classification', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Intelligence Feed")
    st.dataframe(df)

if __name__ == "__main__":
    model = load_intelligence_unit()
    raw_df = get_unified_data()
    run_dashboard(raw_df, model)