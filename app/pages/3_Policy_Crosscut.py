import streamlit as st
from utils.google import generate
from utils.polling import ingest_polling_spreadsheet

st.session_state.output = ""
st.session_state.form_expanded = True

form_expander = st.expander(label="Upload Data", expanded=st.session_state.form_expanded)

with form_expander:
    with st.form(key="crosscut-form", border=False):
        uploaded_file = st.file_uploader("Polling Data (.xlsx)", accept_multiple_files=False)

        policy_brief = st.text_input("Provide the policy brief")

        submitted = st.form_submit_button("Go!")

        if submitted:
            polling_data = ingest_polling_spreadsheet(uploaded_file)
            prompt_template = f"""
                You are a communications adviser: your role is to prepare the Prime Minister for an upcoming appearance where they will brief the media on a policy announcement.
                Only use information presented in this prompt, citing specific statistics by demographic. Do not provide recommendations or messaging strategies, and ensure your output is relevant to the policy brief.

                The Prime Minister will be briefing the following policy announcement: {policy_brief}

                This is an extract from a CSV file containing polling data. Use it to explain how different demographics may react to the policy announcement:
                {polling_data}
                """
            st.session_state.output = generate(prompt_template)
            st.session_state.form_expanded = False
    

st.markdown(st.session_state.output)

