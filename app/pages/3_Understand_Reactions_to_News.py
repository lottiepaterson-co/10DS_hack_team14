import streamlit as st
from utils.google import generate
from utils.news import get_national_news_headlines
from utils.polling import ingest_polling_spreadsheet

st.session_state.output = ""

with st.sidebar:
    with st.form(key="news-form", border=False):
        uploaded_file = st.file_uploader("Polling Data (.xlsx)", accept_multiple_files=False)

        timeframe = st.selectbox(label="Use news articles from the last:", options=["1h", "24h"])

        submitted = st.form_submit_button("Go!")

        if submitted:
            polling_data = ingest_polling_spreadsheet(uploaded_file)
            news_articles = get_national_news_headlines(timeframe)
            prompt_template = f"""
                You are a communications adviser: your role is to prepare the Prime Minister for an upcoming appearance where they will brief the media on a policy announcement.
                Only use information presented in this prompt, citing specific statistics by demographic. Do not provide recommendations or messaging strategies, and ensure your output is relevant to the policy brief.

                This is a set of recent news articles: {news_articles}

                This is an extract from a CSV file containing opinion poll data: {polling_data}

                Using only the provided opinion poll data and news articles, explain how different demographics are likely to react to specific news articles, ensuring you cite the article title and source.
                """
            st.session_state.output = generate(prompt_template)

st.markdown(st.session_state.output)

