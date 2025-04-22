import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
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

# Title and Description
st.title("Data Sweeper Sterling Integrator By Haseeb Abbasi")
st.write("Transform your file between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3!")

# File uploader
uploaded_files = st.file_uploader("Upload your file (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
#file details
st.write(" Preview the head of the Dataframe")
st.dataframe(df.head())

#data cleaning options
st.subheader("Data Cleaning option")
if st.checkbox(f"Clean data for{file.name}"):
    col1, col2 = st.columns(2)

    with col1 : 
        if st.button(f"Remove duplicates from the file : {file.name}"):
            df.drop_duplicates(inplace=True)

            st.write("Duplicates removed")

        with col2 :
            if st.button(f"Fill missing value for : {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing Values have been filled!")
                st.subheader("Select columns to Keep")
columns = st.multiselect(f"Choose columns for{file.name}" , df.columns, default=df.columns)
df = df [columns]

#data visualization
st.subheader("Data Visualization")
if st.checkbox(f"Show visualization for {file.name}"):
    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

 #Conversion Options 
st.subheader("Conversion Option")
conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)        
if st.button(f"Convert{file.name}"):
     Buffer = BytesIO()               
if conversion_type == "CSV" :
     df.to.csv(Buffer , index=False)
     file_name = file.name.replace(file_ext,"csv")
     mime_type ="text/csv"
elif conversion_type =="Excel" :
    df.to.to_excel(Buffer,index=False)
    file_name =file.name.repalce(file_ext,"xlsx")
mime_type = "application/vnd.openxmlformat-officedocument.spreadsheetml.sheet"
Buffer.seek(0)

st.download_button(
    label=f"Download {file.name} as {conversion_type}" ,
    data=Buffer,
    file_name=file_name,
    mime=mime_type
)

st.success("All file  processed successfully! ")
