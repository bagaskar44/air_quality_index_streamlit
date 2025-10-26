import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("WAQI_TOKEN")

STATIONS = {
    "Tangerang": "A515941",
    "Bogor": "A544657",
    "Surabaya": "A420154",
    "Kabupaten Semarang": "A472450",
    "Kabupaten Karawang": "A416773",
    "Solo Manahan": "A416908"
}

def get_station_data(station_name, station_id):
    url = f"https://api.waqi.info/feed/{station_id}/?token={TOKEN}"
    r = requests.get(url).json()
    if r.get("status") != "ok":
        return None

    d = r["data"]
    return {
        "name": station_name,
        "lat": d["city"]["geo"][0],
        "lon": d["city"]["geo"][1],
        "aqi": d["aqi"]
    }

def get_aqi_color(aqi):
    """Return color based on AQI value"""
    if aqi <= 50:
        return '#00e400'  # Good - Green
    elif aqi <= 100:
        return '#ffff00'  # Moderate - Yellow
    elif aqi <= 150:
        return '#ff7e00'  # Unhealthy for Sensitive Groups - Orange
    elif aqi <= 200:
        return '#ff0000'  # Unhealthy - Red
    elif aqi <= 300:
        return '#8f3f97'  # Very Unhealthy - Purple
    else:
        return '#7e0023'  # Hazardous - Maroon

st.title("🌍 Heatmap Kualitas Udara (AQI)")

results = []
for name, sid in STATIONS.items():
    data = get_station_data(name, sid)
    if data:
        results.append(data)

df = pd.DataFrame(results)

st.write("### Data Stasiun")
st.dataframe(df)

# Center map di rata-rata koordinat stasiun
center_lat = df["lat"].mean()
center_lon = df["lon"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# Heatmap dihilangkan - hanya tampilkan label saja

# Add custom marker dengan DivIcon untuk tiap titik
for i, row in df.iterrows():
    aqi_color = get_aqi_color(row['aqi'])
    
    # Create custom HTML for the marker
    html = f"""
    <div style="
        background-color: {aqi_color};
        color: black;
        font-weight: bold;
        font-size: 14px;
        # Modifikasi padding dan tambahkan min-width
        padding: 5px 15px; /* Menambah padding horizontal dari 10px menjadi 15px */
        min-width: 40px; /* Menjamin lebar minimum kotak */
        border-radius: 5px;
        border: 2px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        text-align: center;
        white-space: nowrap;
        # Tambahan: Atur agar angka lebih rapi di tengah dengan menyesuaikan DivIcon style jika diperlukan
        line-height: 1.2;
    ">
        {int(row['aqi'])}
    </div>
    """
    
    folium.Marker(
        location=[row["lat"], row["lon"]],
        icon=folium.DivIcon(html=html),
        popup=f"<b>{row['name']}</b><br>AQI: {row['aqi']}"
    ).add_to(m)

st.write("### Peta Kualitas Udara")
st_folium(m, width=700, height=500)

# Legend
st.write("### Legenda AQI")
legend_df = pd.DataFrame({
    "AQI Range": ["0-50", "51-100", "101-150", "151-200", "201-300", "300+"],
    "Category": ["Good", "Moderate", "Unhealthy for Sensitive", "Unhealthy", "Very Unhealthy", "Hazardous"],
    "Color": ["🟢", "🟡", "🟠", "🔴", "🟣", "🟤"]
})
st.dataframe(legend_df, hide_index=True)