import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page setup
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Sweeper Sterling Integrator By Haseeb Abbasi")
st.write("Transform your file between CSV and Excel formats with built-in data cleaning and visualization. Project for Quarter 3!")

# File uploader
uploaded_files = st.file_uploader("Upload your file (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Process uploaded files
if uploaded_files:
    for i, file in enumerate(uploaded_files):
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # ✅ Safe preview inside the loop (fix for line 42)
        st.subheader(f"📄 Preview: {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed.")

            with col2:
                if st.button(f"Fill missing values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled with column mean.")

        # Column selection
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show chart for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"conversion_{i}")

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            file_output_name = ""

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_output_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_output_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {file_output_name}",
                data=buffer,
                file_name=file_output_name,
                mime=mime_type
            )

    st.success("🎉 All files processed successfully!")
else:
    st.info("Please upload at least one CSV or Excel file to begin.")
