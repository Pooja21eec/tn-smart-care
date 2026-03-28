import pandas as pd
import streamlit as st

# PAGE CONFIG
st.set_page_config(page_title="TN Smart Care X", layout="wide")
st.markdown("""
<style>
/* Background */
body {
    background-color: #f5f7fb;
}

/* Card style */
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

/* Title */
h1 {
    color: #2c3e50;
    text-align: center;
}

/* Button */
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)
# HEADER
st.title("🏥 TN Smart Care X")
st.markdown("### AI Powered Healthcare Decision System")
st.markdown("---")

# INPUTS
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    spo2 = st.number_input("🩸 SpO2 Level", value=95)
    heart_rate = st.number_input("❤️ Heart Rate", value=80)

with col2:
    patient_lat = st.number_input("📍 Latitude", value=13.067)
    patient_lon = st.number_input("📍 Longitude", value=80.237)

st.markdown('</div>', unsafe_allow_html=True)

# HOSPITAL DATA
hospitals = [
    {"name": "Apollo", "distance": 5, "icu_beds": 2, "lat": 13.060, "lon": 80.250},
    {"name": "Global", "distance": 8, "icu_beds": 5, "lat": 13.080, "lon": 80.270},
    {"name": "City", "distance": 3, "icu_beds": 0, "lat": 13.050, "lon": 80.240}
]

df = pd.DataFrame(hospitals)

# FUNCTIONS
def predict_priority(spo2, heart_rate):
    if spo2 < 90:
        return "HIGH"
    elif spo2 < 95:
        return "MEDIUM"
    else:
        return "LOW"


def select_hospital(priority):
    available = [h for h in hospitals if h["icu_beds"] > 0]

    if priority == "HIGH":
        available.sort(key=lambda x: x["distance"])
    else:
        available.sort(key=lambda x: (-x["icu_beds"], x["distance"]))

    return available[0]


def ambulance_time(distance):
    return round((distance / 40) * 60, 2)


def icu_monitor(spo2, heart_rate):
    if spo2 < 90:
        return "CRITICAL 🚨"
    elif heart_rate > 120 or heart_rate < 50:
        return "WARNING ⚠️"
    else:
        return "STABLE ✅"


# BUTTON
st.markdown("---")

if st.button("🚑 Get Smart Decision"):

    # ⏳ LOADING ANIMATION (FIRST)
    with st.spinner("Analyzing patient data..."):
        import time
        time.sleep(1)

    # LOGIC
    priority = predict_priority(spo2, heart_rate)
    selected = select_hospital(priority)
    eta = ambulance_time(selected["distance"])
    icu_status = icu_monitor(spo2, heart_rate)

    # 🎨 RESULT CARD
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(f"""
    ### 🚨 Priority: {priority}
    ### 🏥 Hospital: {selected['name']}
    ### 🚑 ETA: {eta} minutes
    ### 🧬 ICU Status: {icu_status}
    """)

    st.markdown('</div>', unsafe_allow_html=True)

    # 📊 DASHBOARD CARD
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 System Dashboard")

    st.bar_chart(df.set_index("name")["icu_beds"])

    health_data = pd.DataFrame({
        "Metric": ["SpO2", "Heart Rate"],
        "Value": [spo2, heart_rate]
    })

    st.bar_chart(health_data.set_index("Metric"))

    st.markdown('</div>', unsafe_allow_html=True)

    # 🌍 MAP CARD
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🌍 Ambulance Tracking")

    map_data = {
        "lat": [patient_lat, selected["lat"]],
        "lon": [patient_lon, selected["lon"]]
    }

    st.map(map_data)

    st.markdown('</div>', unsafe_allow_html=True)
