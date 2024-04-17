import streamlit as st
from utils.google import generate
from utils.news import get_local_news_headlines

st.session_state.output = """
# Understand Local News

Summarise local news stories for the location you're visiting from the last 1h or 24h.

:point_left: Get started!
"""

with st.sidebar:
    with st.form(key="news-form", border=False):

        placename = st.text_input(label="Where are you visiting?")

        timeframe = st.selectbox(label="Use news articles from the last:", options=["1h", "24h"])

        submitted = st.form_submit_button("Go!")

        if submitted:
            county = generate(f"Which UK county is {placename} in? Respond only with the name of the county.").rstrip()
            news_articles = get_local_news_headlines(county, timeframe)
            prompt_template = f"""
                You are a communications adviser: your role is to prepare the Prime Minister for an upcoming appearance where they will face questions from the media.
                Only use information presented in this prompt, citing specific news articles. Do not provide recommendations or messaging strategies.

                This is a set of recent news articles: {news_articles}

                Summarise the provided news articles, and suggest questions that may be asked based only on the articles ensuring you cite the article title and source.
                """
            st.session_state.output = generate(prompt_template)

st.markdown(st.session_state.output)

