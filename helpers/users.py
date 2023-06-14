from db import *

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

def get_user(user_id):
    user = session.query(User).filter(User.user_id.ilike(f'%{user_id}%')).first()
    return user

# Helper function to get all users
def get_all_users():
    users = session.query(User)
    return users