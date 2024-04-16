import streamlit as st

from docx import Document

from utils.google import generate
from utils.polling import ingest_polling_spreadsheet

st.session_state.output = ""
st.session_state.polling_spreadsheet = None
st.session_state.policy_detail = None

with st.sidebar:
    with st.form(key="policy-form", border=False):
        st.session_state.polling_spreadsheet = st.file_uploader("Polling Data (.xlsx)")

        st.session_state.policy_detail = st.text_area("Paste the text of the policy announcement here")

        submitted = st.form_submit_button("Go!")

        if submitted:
            if (st.session_state.polling_spreadsheet is None) or (st.session_state.policy_detail is None):
                st.warning("You must provide both a spreadsheet of polling data, and a policy announcement")
                st.stop()
            polling_data = ingest_polling_spreadsheet(st.session_state.polling_spreadsheet)
            policy_brief = st.session_state.policy_detail

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

