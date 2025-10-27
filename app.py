import streamlit as st
import preprocessor

st.sidebar.title("What'sapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    st.dataframe(df)
    