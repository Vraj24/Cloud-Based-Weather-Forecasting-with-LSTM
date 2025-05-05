import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# === App Title ===
st.title("📊 7-Day Weather Forecast Dashboard")
st.markdown("This dashboard visualizes forecasted weather data from your cleaned dataset.")

# === Load Data ===
uploaded_file = st.file_uploader("📁 Upload the forecast CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("✅ File loaded successfully!")

    # === Show Columns ===
    st.subheader("📋 Columns in the dataset")
    st.write(df.columns.tolist())

    # === Check for 'Day' or 'Date' column ===
    if 'Day' in df.columns:
        x_axis = df['Day']
        x_label = "Day"
    elif 'Date' in df.columns:
        x_axis = df['Date']
        x_label = "Date"
    else:
        st.error("❌ Neither 'Day' nor 'Date' column is present in the dataset.")
        st.stop()

    # === Feature Columns ===
    excluded_columns = ['Day', 'Date']
    features = [col for col in df.columns if col not in excluded_columns]

    # === Plot each feature ===
    for feature in features:
        st.subheader(f"📈 {feature} — 7-Day Forecast")
        fig, ax = plt.subplots()
        ax.plot(x_axis, df[feature], marker='o', linestyle='-')
        ax.set_xlabel(x_label)
        ax.set_ylabel(feature)
        ax.set_title(f"{feature} over the Next 7 Days")
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

else:
    st.warning("📂 Please upload a forecasted CSV file to begin.")
