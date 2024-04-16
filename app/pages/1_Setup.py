import streamlit as st

from utils.google import generate

with st.form(key="setup-form"):
    uploaded_files = st.file_uploader("Upload polling data spreadsheet", accept_multiple_files=True)

    policy_brief = st.text_input("Provide the policy brief")

    other_issues = st.text_input("What other issues are in the news?")

    submitted = st.form_submit_button("Do generative AI")

    if submitted:
        st.session_state.policy_brief = policy_brief
        st.session_state.other_issues = other_issues
        st.session_state.polling_data = uploaded_files
        st.session_state.output = generate()