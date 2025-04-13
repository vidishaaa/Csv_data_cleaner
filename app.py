import pandas as pd
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="CSV Data Cleaner",
    page_icon="🧹",
    layout="centered"
)

# --- Custom CSS Styling ---
def local_css():
    st.markdown("""
        <style>
            body {
                background-image: linear-gradient(to right, #e0f7fa, #f1f8e9);
                font-family: 'Segoe UI', sans-serif;
            }
            .title {
                font-size: 40px !important;
                font-weight: bold;
                color: #2E8B57;
                text-align: center;
            }
            .subtitle {
                font-size: 20px;
                color: #555;
                margin-bottom: 15px;
            }
            .stButton>button, .stDownloadButton>button {
                background-color: #2E8B57;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 20px;
            }
        </style>
    """, unsafe_allow_html=True)

local_css()

st.markdown('<div class="title">🧹 CSV Data Cleaner</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Clean messy CSVs — handle nulls, remove duplicates, and more!</p>', unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

# --- Null Handling Logic ---
def handle_nulls(df, method):
    if method == "Drop rows with nulls":
        df = df.dropna()
    elif method == "Fill with N/A":
        df = df.fillna("N/A")
    elif method == "Fill with 0":
        df = df.fillna(0)
    elif method == "Fill with column mean":
        df = df.fillna(df.mean(numeric_only=True))
    elif method == "Fill with column median":
        df = df.fillna(df.median(numeric_only=True))
    elif method == "Drop columns with >50% nulls":
        threshold = len(df) * 0.5
        df = df.dropna(thresh=threshold, axis=1)
    return df

# --- Cleaning Function ---
def clean_csv(file, null_option):
    try:
        df = pd.read_csv(file)

        st.markdown("### 📌 Original Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Clean column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Drop duplicates
        df.drop_duplicates(inplace=True)

        # Drop fully empty rows/cols
        df.dropna(how="all", inplace=True)
        df.dropna(axis=1, how="all", inplace=True)

        # Null handling
        df = handle_nulls(df, null_option)

        st.success("✅ Cleaning Complete!")
        st.markdown("### ✨ Cleaned Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        return df

    except Exception as e:
        logging.error(f"Error: {e}")
        st.error(f"🚨 Error cleaning CSV: {e}")
        return None

# --- App Logic ---
if uploaded_file:
    st.markdown("### 🧪 Choose how to handle NULL values")
    null_option = st.selectbox("How should we handle missing values?", [
        "Drop rows with nulls",
        "Fill with N/A",
        "Fill with 0",
        "Fill with column mean",
        "Fill with column median",
        "Drop columns with >50% nulls"
    ])

    # Add a button to trigger the cleaning process
    if st.button("Start Cleaning Process", key="clean_button"):
        cleaned_df = clean_csv(uploaded_file, null_option)

        if cleaned_df is not None:
            cleaned_csv = cleaned_df.to_csv(index=False).encode("utf-8")

            st.markdown("### 📥 Download Your Cleaned CSV")
            st.download_button(
                label="Download Cleaned File",
                data=cleaned_csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )
    else:
        st.info("👆 Select your null handling option and click 'Start Cleaning Process' to begin.")
else:
    st.info("👆 Upload a CSV file to get started.")

st.markdown("---")
st.markdown(
    "<center><small>Made for Open Source Tech Project</small></center>",
    unsafe_allow_html=True
)
