import streamlit as st
from utils.google import generate
from utils.polling import ingest_polling_spreadsheet

st.session_state.generic_summary ="""
# Understanding Polling Data

Get a summary of polling data of your choice to understand the differences between different demographics and interest groups.

:point_left: Get started!
"""
st.session_state.summary_form_expanded = True

form_expander = st.expander(label="Upload Data", expanded=st.session_state.summary_form_expanded)

with st.sidebar:
    with st.form(key="summary-form", border=False):
        uploaded_file = st.file_uploader("Polling Data (.xlsx)", accept_multiple_files=False)

        submitted = st.form_submit_button("Go!")

        if submitted:
            polling_data = ingest_polling_spreadsheet(uploaded_file)
            prompt_template = f"""
                This is an extract from a CSV file containing polling data. Summarise it:
                {polling_data}
                """
            st.session_state.generic_summary = generate(prompt_template)
            st.session_state.summary_form_expanded = False
    

st.markdown(st.session_state.generic_summary)

