from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

# Create the database engine
engine = create_engine('sqlite:///db/dokbackend.db')

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

    door_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    openable_by = Column(String)


# Define the DoorAccess model
class DoorAccess(Base):
    __tablename__ = 'door_access'

    access_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.user_id'))
    door_id = Column(String, ForeignKey('doors.door_id'))
    accessed_at = Column(DateTime, default=func.now())

    user = relationship("User", backref="accesses")
    door = relationship("Door", backref="accesses")


# Define the News model
class News(Base):
    __tablename__ = 'news'

    news_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(String, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=func.now())
    topic = Column(String)
    title = Column(String)
    content = Column(String)

    author = relationship("User", backref="news")


# Define the Tasks model
class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(String, ForeignKey('users.user_id'))
    assigned_to = Column(String)
    description = Column(String)
    deadline = Column(DateTime)
    isdone = Column(Boolean, default=False)
    experience = Column(String)

    author = relationship("User", backref="tasks")


# Define the Votes model
class Vote(Base):
    __tablename__ = 'votes'

    vote_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
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

    message_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(String, ForeignKey('users.user_id'))
    sent_at = Column(DateTime, default=func.now())
    content = Column(String)

    author = relationship("User", backref="messages")


# Create the tables in the database
Base.metadata.create_all(engine)




