#import relevant packages
import pandas as pd
import requests

def get_national_news_headlines(time_frame):
#timeframe should be 1h or 24h, default is 1h

    #set the parametres and set up API key for the newscatcher API
    url = 'https://v3-api.newscatcherapi.com/api/latest_headlines?'
    #themes = ['Business', 'Economics', 'Finance', 'Health', 'Politics', 'Science', 'Tech', 'Crime', 'General']
    themes = ['Health, Business, Finance, Economics, Politics, Crime, Science, Tech, General, Travel']
    params = { 'q': '*','lang': 'en', 'countries': 'GB', 'when':'1h', 'page_size': 100, 'sort_by': 'relevancy', 'is_headline': True, 'ranked_only': True, 'clustering_enabled': False, 'theme': themes, 'sources':'bbc.co.uk, theguardian.com, telegraph.co.uk, times.co.uk, dailymail.co.uk, standard.co.uk, metro.co.uk, mirror.co.uk, sundaytimes.co.uk'}
    params['when']= time_frame
    headers = {'x-api-token': '0OV147hPPeTT6S1vpRWiYvN4nDvsa1EN'}
    #Call the API to generate clusters of UK news headlines from the past hour from national newspapers
    response = requests.get(url, params=params, headers=headers)

    #Manipulate the results to produce a dataframe showing the title of articles in each cluster, the content of the articles and their sources.
    data = response.json()
    total_pages = data['total_pages']
    current_page = 1
    compiled_headlines = []
    while current_page < total_pages + 1:
        if current_page > 1:
            params['page'] = current_page
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
        for article in data['articles']:
                compiled_headlines.append([article['title'], article['name_source'], article['content']])
        current_page = current_page +1

    df = pd.DataFrame(compiled_headlines)
    df.columns = ['Title', 'Source', 'Content']
    return df.to_string()

def get_local_news_headlines(county, timeframe):

    county_news_matching = pd.read_csv("app/static/20240416 - Collection-38381111-United Kingdom - State & Local-sources-.csv")
    news_sources = county_news_matching[county_news_matching['county_full']==county]['homepage']
    sources_list = ', '.join(news_sources.tolist())
    sources_list = sources_list.replace('http://', '')
    sources_list = sources_list.replace('/', ' ')


    #set the parametres and set up API key for the newscatcher API
    url = 'https://v3-api.newscatcherapi.com/api/latest_headlines?'
    #themes = ['Business', 'Economics', 'Finance', 'Health', 'Politics', 'Science', 'Tech', 'Crime', 'General']
    themes = ['Health, Business, Finance, Economics, Politics, Crime, Science, Tech']
    params = { 'q': '*','lang': 'en', 'countries': 'GB', 'when':timeframe, 'page_size': 100, 'sort_by': 'relevancy', 'is_headline': True, 'ranked_only': True, 'clustering_enabled': False, 'theme': themes, 'sources':sources_list}
    headers = {'x-api-token': '0OV147hPPeTT6S1vpRWiYvN4nDvsa1EN'}
    #Call the API to generate clusters of UK news headlines from the past twenty four hours
    response = requests.get(url, params=params, headers=headers)

    #Manipulate the results to produce a dataframe showing the title of articles in each cluster, the content of the articles and their sources.
    data = response.json()
    total_pages = data['total_pages']
    current_page = 1
    compiled_headlines = []
    while current_page < total_pages + 1:
        if current_page > 1:
            params['page'] = current_page
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
        for article in data['articles']:
            compiled_headlines.append([article['title'], article['content'], article['name_source']])
        current_page = current_page +1

    return compiled_headlines