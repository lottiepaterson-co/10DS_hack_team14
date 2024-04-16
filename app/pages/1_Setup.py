import streamlit as st

from utils.google import generate
from utils.polling import ingest_polling_spreadsheet

st.session_state["polling_data"] = ""
st.session_state["output"] = ""

with st.form(key="setup-form"):
    uploaded_file = st.file_uploader("Upload polling data spreadsheet", accept_multiple_files=False)

    policy_brief = st.text_input("Provide the policy brief")

    other_issues = st.text_input("What other issues are in the news?")

    submitted = st.form_submit_button("Do generative AI")

    if submitted:
        st.session_state.policy_brief = policy_brief
        st.session_state.other_issues = other_issues
        st.session_state.polling_data = ingest_polling_spreadsheet(uploaded_file)
        st.session_state.output = generate(prompt=f"""This is an extract from a csv containing opinion poll data. Summarise it: {st.session_state.polling_data}""")