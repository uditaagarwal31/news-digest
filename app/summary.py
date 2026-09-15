import os
from dotenv import load_dotenv
from anthropic import Anthropic
import json


# load_dotenv()
# client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# response = client.messages.create(
#     model="claude-haiku-4-5-20251001",
#     max_tokens=200,
#     messages=[
#         {"role": "user", "content": "Summarize this in one sentence: The Federal Reserve raised interest rates by 0.25% on Tuesday, citing persistent inflation concerns."}
#     ]
# )
# print(response.content)
# #print(response.content[0].text)


def summarise_article(articles):
    load_dotenv()
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    articles_block = ""
    articles_titles_block = []
    for i, article in enumerate(articles):
        articles_block += f"{i+1}. Title: {article.title}\nContent: {article.content}\n\n"
        articles_titles_block.append(article.title)

    prompt = f"""Summarize each of these {len(articles)} articles in 2 sentences each, as a text message a user would read. Provide enough context about the article though so that the user can
        make conversation about it.
        {articles_block}
        Return ONLY a JSON array of strings, one summary per article, in the same order given. No preamble, no markdown, no explanation — just the JSON array."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text = response.content[0].text

    try:
        summaries = json.loads(text)
    except json.JSONDecodeError:
        # Claude wrapped it in markdown fences — strip them and retry
        cleaned = text.strip() # removes trailing white spaces/newlines 
        cleaned = cleaned.removeprefix("```json").removeprefix("```") # removes json if string starts with it, nothing otherwise
        cleaned = cleaned.removesuffix("```") # removes closing fence in the end
        cleaned = cleaned.strip() # removes whatever whitespace/newlines is left
        summaries = json.loads(cleaned)

    print(articles_titles_block,summaries)

    return (articles_titles_block,summaries)