# Helper function to create a new user
from db import *

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