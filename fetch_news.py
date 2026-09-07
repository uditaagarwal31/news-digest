import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import json

load_dotenv()  # reads .env and loads its variables into the environment

newsapi = NewsApiClient(os.getenv("NEWSAPI_KEY"))

countries = ['us', 'india', 'europe', 'china']

categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

# create array of user countries
# array of user categories
# put forloop to get all possible responses
# add responses in a data structure

top_headlines_response = newsapi.get_top_headlines(
    category='business',
    language='en',
    country='us'
)


for article in top_headlines_response["articles"]:
    print(article["title"], article["content"], article["url"])
