from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

# Create the database engine
engine = create_engine('sqlite:///dokbackend.db')

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    name = Column(String)
    joined_at = Column(DateTime, default=func.now())
    auth_level = Column(Integer, default=0)


# Define the Door model
class Door(Base):
    __tablename__ = 'doors'

    door_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String)
    auth_level_needed = Column(Integer)


# Define the DoorAccess model
class DoorAccess(Base):
    __tablename__ = 'door_access'

    access_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.user_id'))
    door_id = Column(String, ForeignKey('doors.door_id'))
    accessed_at = Column(DateTime, default=func.now())

    user = relationship("User", backref="accesses")
    door = relationship("Door", backref="accesses")


# Define the News model
class News(Base):
    __tablename__ = 'news'

    news_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    author_id = Column(String, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=func.now())
    content = Column(String)

    author = relationship("User", backref="news")


# Define the Tasks model
class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    author_id = Column(String, ForeignKey('users.user_id'))
    assigned_to = Column(String)  # Can be a comma-separated string of user_ids
    description = Column(String)
    deadline = Column(DateTime)

    author = relationship("User", backref="tasks")


# Define the Votes model
class Vote(Base):
    __tablename__ = 'votes'

    vote_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    author_id = Column(String, ForeignKey('users.user_id'))
    content = Column(String)
    vote_y = Column(Integer)
    vote_n = Column(Integer)

    @property
    def vote_total(self):
        return 0 + self.vote_y - self.vote_n


# Define the Chat model
class Chat(Base):
    __tablename__ = 'chat'

    message_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    author_id = Column(String, ForeignKey('users.user_id'))
    sent_at = Column(DateTime, default=func.now())
    content = Column(String)

    author = relationship("User", backref="messages")


# Create the tables in the database
Base.metadata.create_all(engine)


# Helper function to create a new user
def create_user(name, user_id):
    user = User(name=name, user_id=user_id)
    session.add(user)
    session.commit()
    return user

# Helper function to delete a user
def delete_user(user_id):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()

# Helper function to search for users by name
def get_user_exist(user_id):
    user = session.query(User).filter(User.user_id.ilike(f'%{user_id}%')).first()
    return user is not None

# Helper function to create a new door
def create_door(name, auth_level_needed):
    door = Door(name=name, auth_level_needed=auth_level_needed)
    session.add(door)
    session.commit()
    return door

# Helper function to delete a door
def delete_door(door_id):
    door = session.query(Door).get(door_id)
    if door:
        session.delete(door)
        session.commit()

# Helper function to search for doors by name
def search_doors_by_name(name):
    doors = session.query(Door).filter(Door.name.ilike(f'%{name}%')).all()
    return doors

# Helper function to create a new door access
def create_door_access(user_id, door_id):
    door_access = DoorAccess(user_id=user_id, door_id=door_id)
    session.add(door_access)
    session.commit()
    return door_access

# Helper function to delete a door access
def delete_door_access(access_id):
    door_access = session.query(DoorAccess).get(access_id)
    if door_access:
        session.delete(door_access)
        session.commit()

# Helper function to create a new news
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

# Helper function to search tasks assigned to a user
def search_tasks_by_user(user_id):
    tasks = session.query(Task).filter(Task.assigned_to.ilike(f'%{user_id}%')).all()
    return tasks

# Helper function to create a new task
def create_task(author_id, assigned_to, description, deadline):
    task = Task(author_id=author_id, assigned_to=assigned_to, description=description, deadline=deadline)
    session.add(task)
    session.commit()
    return task

# Helper function to delete a task
def delete_task(task_id):
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()

# Helper function to create a new vote
def create_vote(author_id, content, vote_y, vote_n):
    vote = Vote(author_id=author_id, content=content, vote_y=vote_y, vote_n=vote_n)
    session.add(vote)
    session.commit()
    return vote

# Helper function to delete a vote
def delete_vote(vote_id):
    vote = session.query(Vote).get(vote_id)
    if vote:
        session.delete(vote)
        session.commit()


# Helper function to create a new chat message
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


# Helper function to search for chat messages by content
def search_chat_messages_by_content(content):
    messages = session.query(Chat).filter(Chat.content.ilike(f'%{content}%')).all()
    return messages
