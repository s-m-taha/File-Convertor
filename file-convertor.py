import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Convertor", layout="wide")
st.title("File Convertor & Cleaner")
st.write(
    "This is a simple file convertor and cleaner tool. You can upload a file and convert it to a different format. You can also clean the data by removing empty rows and columns."
)
files = st.file_uploader(
    "UPLOAD CSV OR EXCEL FILE.", type=["csv", "xlsx"], accept_multiple_files=True
)
if files:
    for file in files:
        ext = file.name.split(".")[-1]
        if ext == "csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        st.subheader(f"{file.name} - Preview")
        st.write(df.head())
        if st.checkbox(f"remove duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("removed duplicates")
            st.dataframe(df.head())

        if st.checkbox(f"fill missing values - {file.name}"):
            for col in df.select_dtypes(include=["number"]).columns:
                df[col] = df[col].fillna(df[col].mean())
            st.success("filled missing values with means")
            st.dataframe(df.head())

        selected_columns = st.multiselect(
            f"select columns - {file.name}", df.columns, default=df.columns.tolist()
        )
        df = df[selected_columns]
        st.dataframe(df.head())

        if (
            st.checkbox(f"show chart - {file.name}")
            and not df.select_dtypes(include="number").empty
        ):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(
            f"convert {file.name} to:", ["csv", "Excel"], key=file.name
        )
        if st.button(f"download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")
            output.seek(0)
            st.download_button(
                label=f"Download {new_name}",
                data=output.read(),
                file_name=new_name,
                mime=mime,
            )
            st.success(f"file converted successfully: {new_name}")
               
                