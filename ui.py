import pandas as pd
import streamlit as st
import joblib
import datetime
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import plotly.express as px

# 🌌 Global dark theme background and logo header
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://www.adlittle.com/sites/default/files/viewpoints/flexibility-services-catch-me-if-you-can.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main > div {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        padding: 1.5rem;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 🖼️ About page styling
def set_about_background():
    st.markdown("""
        <style>
        .about-page {
            background-image: url("https://www.adlittle.com/sites/default/files/viewpoints/flexibility-services-catch-me-if-you-can.jpg");
            background-size: cover;
            background-position: center;
            padding: 2rem;
            border-radius: 10px;
            color: white;
        }
        .logo {
            display: block;
            margin: auto;
            width: 100px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

# 🔀 Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Predict", "Dashboard", "About"],
        icons=["house", "bar-chart", "clipboard-data", "info-circle"],
        default_index=1
    )

# 📦 Load both models
models = {
    "Random Forest": joblib.load("E:\energy consumption\Random_forest_model (2).pkl"),
    "Linear Regression": joblib.load("E:\energy consumption\Linear-model.pkl")
}

# 🔧 Expected input features
model_columns = [
    'num_occupants', 'house_size_sqft', 'monthly_income', 'outside_temp_celsius',
    'year', 'month', 'day', 'season',
    'heating_type_Electric', 'heating_type_Gas', 'heating_type_None',
    'cooling_type_AC', 'cooling_type_Fan', 'cooling_type_None',
    'manual_override_Y', 'manual_override_N', 'is_weekend', 'temp_above_avg',
    'income_per_person', 'square_feet_per_person', 'high_income_flag', 'low_temp_flag',
    'season_spring', 'season_summer', 'season_fall', 'season_winter',
    'day_of_week_0', 'day_of_week_6', 'energy_star_home'
]

# 🏠 Home Page
if selected == "Home":
    st.title("🏠 Welcome to the Energy Consumption Predictor")
    st.markdown("""
    This app helps you estimate energy usage based on household factors.
    
    **Navigation Overview**:
    - 🔍 Predict energy usage
    - 📊 Visualize and analyze predictions
    - ℹ️ Learn about the app
    """)

# ⚡ Predict Page
elif selected == "Predict":
    st.title("⚡ Energy Consumption Prediction")

    

    col1, col2 = st.columns(2)
    with col1:
        num_occupants = st.number_input("Number of occupants", min_value=1, value=3)
        house_size_sqft = st.number_input("House sqft", min_value=500, value=2000)
        monthly_income = st.number_input("Monthly income", min_value=1000, value=5000)
        outside_temp_celsius = st.number_input("Temperature (°C)", min_value=-10, value=27)
    with col2:
        year = st.number_input("Year", min_value=2000, value=2024)
        month = st.number_input("Month", min_value=1, max_value=12, value=7)
        day = st.number_input("Day", min_value=1, max_value=31, value=10)
        heating_type = st.selectbox("Heating Type", options=["Electric", "Gas", "None"])
        cooling_type = st.selectbox("Cooling Type", options=["AC", "Fan", "None"])
        manual_override = st.radio("Manual Override", options=["Y", "N"])
        energy_star_home = st.checkbox("Energy Star Certified")

    obj = datetime.date(year, month, day)
    day_of_week = obj.weekday()
    season_label = (
        "Winter" if month in [12, 1, 2, 3] else
        "Summer" if month in [4, 5, 6] else
        "Rainy" if month in [7, 8, 9] else "Monsoon"
    )

    is_weekend = int(day_of_week >= 5)
    temp_above_avg = int(outside_temp_celsius > 28)
    income_per_person = monthly_income / num_occupants
    square_feet_per_person = house_size_sqft / num_occupants
    high_income_flag = int(monthly_income > 40000)
    low_temp_flag = int(outside_temp_celsius < 28)

    input_data = {
        'num_occupants': num_occupants,
        'house_size_sqft': house_size_sqft,
        'monthly_income': monthly_income,
        'outside_temp_celsius': outside_temp_celsius,
        'year': year, 'month': month, 'day': day,
        'season': {'Winter': 1, 'Summer': 2, 'Rainy': 3, 'Monsoon': 4}[season_label],
        'heating_type_Electric': int(heating_type == "Electric"),
        'heating_type_Gas': int(heating_type == "Gas"),
        'heating_type_None': int(heating_type == "None"),
        'cooling_type_AC': int(cooling_type == "AC"),
        'cooling_type_Fan': int(cooling_type == "Fan"),
        'cooling_type_None': int(cooling_type == "None"),
        'manual_override_Y': int(manual_override == "Y"),
        'manual_override_N': int(manual_override == "N"),
        'is_weekend': is_weekend,
        'temp_above_avg': temp_above_avg,
        'income_per_person': income_per_person,
        'square_feet_per_person': square_feet_per_person,
        'high_income_flag': high_income_flag,
        'low_temp_flag': low_temp_flag,
        'season_spring': int(season_label == "Spring"),
        'season_summer': int(season_label == "Summer"),
        'season_fall': int(season_label == "Fall"),
        'season_winter': int(season_label == "Winter"),
        'day_of_week_0': int(day_of_week == 0),
        'day_of_week_6': int(day_of_week == 6),
        'energy_star_home': int(energy_star_home)
    }

    input_df = pd.DataFrame([input_data])[model_columns]
    model_choice = st.selectbox("Select Model", options=list(models.keys()))
    model = models[model_choice]

    if st.button("Predict"):
        prediction = model.predict(input_df)[0]
        st.success(f"🔋 Predicted Energy Consumption: {prediction:.2f} units")

        st.session_state.update({
            'input_data': input_data,
            'prediction': prediction,
            'income_per_person': income_per_person,
            'square_feet_per_person': square_feet_per_person,
            'temp_above_avg': temp_above_avg,
            'high_income_flag': high_income_flag,
            'is_weekend': is_weekend
        })

        # 🔍 Insights and suggestions
        st.subheader("📌 Insights Based on Your Inputs")
        if temp_above_avg:
            st.info("🌡️ High temperature may raise cooling costs (especially if AC is used).")
        if heating_type == "Electric":
            st.info("⚠️ Electric heating increases consumption significantly during cold weather.")
        if cooling_type == "AC":
            st.info("❄️ AC usage contributes to higher consumption.")
        if num_occupants > 4:
            st.info("👨‍👩‍👧‍👦 Larger households typically consume more energy.")
        if not energy_star_home:
            st.info("🏠 Energy Star certified homes can reduce overall consumption.")
        if manual_override == "Y":
            st.info("🛠️ Manual override may lead to suboptimal energy usage.")
        if high_income_flag:
            st.info("💰 Higher income may correlate with larger homes and higher appliance usage.")

# 📊 Dashboard Page
elif selected == "Dashboard":
    st.title("📊 Dashboard Insights")

    if "input_data" in st.session_state:
        tab1, tab2 = st.tabs(["Derived Features", "Model Inputs"])
        
        with tab1:
            st.metric("Income per person", f"{st.session_state.income_per_person:.2f}")
            st.metric("Sq ft per person", f"{st.session_state.square_feet_per_person:.2f}")
            st.metric("Above avg temp", "✅ Yes" if st.session_state.temp_above_avg else "❌ No")
            st.metric("High income", "✅ Yes" if st.session_state.high_income_flag else "❌ No")
            st.metric("Weekend", "✅ Yes" if st.session_state.is_weekend else "❌ No")

        with tab2:
            input_df = pd.DataFrame([st.session_state.input_data])
            st.dataframe(input_df, use_container_width=True)

            csv = input_df.to_csv(index=False).encode("utf-8")
            st.download_button("📎 Download CSV", data=csv, file_name="input_data.csv", mime="text/csv")

            st.subheader("🎨 Select a Visualization")
            viz_option = st.selectbox("Choose a visualization type:", ["Bar Chart", "Radar Chart", "Pie Chart"])

            if viz_option == "Bar Chart":
                colors = ['mediumseagreen' if val >= 0 else 'tomato' for val in input_df.iloc[0]]
                fig = go.Figure(go.Bar(
                    x=input_df.iloc[0], y=input_df.columns,
                    orientation='h', marker_color=colors
                ))
                fig.update_layout(title="🌟 Feature Contributions (Bar Chart)", height=650)
                st.plotly_chart(fig, use_container_width=True)

            elif viz_option == "Radar Chart":
                radar_df = pd.DataFrame({"Feature": input_df.columns, "Value": input_df.iloc[0].values})
                fig = px.line_polar(radar_df, r='Value', theta='Feature', line_close=True)
                fig.update_traces(fill='toself')
                fig.update_layout(title="🌐 Feature Spread (Radar Chart)")
                st.plotly_chart(fig, use_container_width=True)

            elif viz_option == "Pie Chart":
                fig = go.Figure(go.Pie(labels=input_df.columns, values=input_df.iloc[0].abs(), hole=0.3))
                fig.update_layout(title="📈 Feature Distribution (Pie Chart)")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("🚨 Please make a prediction first from the Predict tab.")

# 📘 About Page
elif selected == "About":
    set_about_background()
    st.markdown("""
        <div class="about-page">
            <img class="logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Energy_icon.svg/2048px-Energy_icon.svg.png" />
            <h2>About This App</h2>
            <p>This application predicts household energy consumption based on various lifestyle and environmental factors.
            Built using both Random Forest and Linear Regression models, it offers flexibility in prediction methods and visual analysis.</p>
            <ul>
                <li>🔍 <b>Predict Tab</b>: Input household data and choose a model to forecast energy usage.</li>
                <li>📊 <b>Dashboard Tab</b>: Analyze input influence and download insights.</li>
                <li>🛠️ Features include derived metrics and season/day-based logic.</li>
            </ul>
            <p style="margin-top:1em;">Crafted with ❤️ using Streamlit and Plotly by Sai Pranavi Ptel.</p>
        </div>
    """, unsafe_allow_html=True)
