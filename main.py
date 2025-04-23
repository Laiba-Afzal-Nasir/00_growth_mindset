import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter & Cleaner",page_icon="📁", layout="wide")
st.title("📁 File Converter & Cleaner")
st.write("Upload your CSV and Excel files to convert formats and clean the data easily")

files = st.file_uploader("Upload CSV and Excel Files" ,type=["csv","xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Fill missing values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("Missing values filled successfully!")
            st.dataframe(df.head())

        selected = st.multiselect(f"Select coloumns {file.name}", df.columns, default=df.columns)
        df = df[selected]
        st.dataframe(df.head())

        if st.checkbox(f"Show Chart {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

        download_choice = st.radio(f"Convert {file.name} to -", ["CSV","Excel"], key=file.name)

        if st.button(f"Download your {file.name} as {download_choice}"):
            output = BytesIO()
            if download_choice == "CSV":
                df.to_csv(output,index=False)
                mime = "text/csv"
                new_file_name = file.name.replace(ext,"csv")
            else:
                df.to_excel(output,index=False)
                mime = "application\vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_file_name = file.name.replace(ext,"xlsx")

            output.seek(0)
            st.download_button(f"Download file", file_name=new_file_name, data=output, mime=mime, key=file.name)
        st.success("Congratulations Processing Is Completed!")