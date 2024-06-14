import streamlit as st

st.title("Informations about the repository")

with open("README.md") as readme:
    text = readme.read()

st.markdown(text)