# Helper function to create a new news
from db import *

def create_news(author_id, topic, title, content):
    news = News(author_id=author_id, topic=topic, content=content, title=title)
    session.add(news)
    session.commit()
    return news

def update_news_image_uri(news_id, image_uri):
    news = session.query(News).get(news_id)
    if news:
        news.image_uri = image_uri
        session.commit()
    return news

# Helper function to delete a news
def delete_news(news_id):
    news = session.query(News).get(news_id)
    if news:
        session.delete(news)
        session.commit()

def get_news():
    news = reversed(session.query(News).all())
    formatted_news = []

    for item in news:
        formatted_item = {
            "id": item.news_id,
            "topic": item.topic,
            "title": item.title,
            "content": item.content,
            "image_uri": f"/get_news_image/{item.news_id}",
        }
        formatted_news.append(formatted_item)

    return formatted_news
