import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
import json
from sqlalchemy.orm import Session

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

#print(top_headlines_response["articles"][0])

for article in top_headlines_response["articles"]:
    print(article["title"], article["content"], article["url"])

#   article_id: auto increment
#    title: Mapped[str] = title
#    url: Mapped[str] = url
#    source: Mapped[str] = source["name"]
#    published_date: publishedAt
#    content: Mapped[str] = content

# print(top_headlines_response["articles"][0]["title"])
# print(top_headlines_response["articles"][0]["url"])
# print(top_headlines_response["articles"][0]["source"]["name"])
# print(top_headlines_response["articles"][0]["publishedAt"])
# print(top_headlines_response["articles"][0]["content"])


