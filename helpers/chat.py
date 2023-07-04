# Helper function to create a new chat message
from db import *

def create_chat_message(author_id, content):
    chat_message = Chat(author_id=author_id, content=content)
    session.add(chat_message)
    session.commit()
    return chat_message

# Helper function to delete a chat message
def delete_chat_message(message_id):
    chat_message = session.query(Chat).get(message_id)
    if chat_message:
        session.delete(chat_message)
        session.commit()
        return True
    return False

# Helper function to search for chat messages by content
def search_chat_messages_by_content(content):
    messages = session.query(Chat).filter(Chat.content.ilike(f'%{content}%')).all()
    return messages