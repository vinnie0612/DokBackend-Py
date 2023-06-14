# Helper function to create a new news
from db import *

def create_news(author_id, content):
    news = News(author_id=author_id, content=content)
    session.add(news)
    session.commit()
    return news

# Helper function to delete a news
def delete_news(news_id):
    news = session.query(News).get(news_id)
    if news:
        session.delete(news)
        session.commit()