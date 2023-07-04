# Helper function to create a new vote
from db import *

def create_vote(author_id, content):
    vote = Vote(author_id=author_id, content=content)
    session.add(vote)
    session.commit()
    return vote

# Helper function to delete a vote
def delete_vote(vote_id):
    vote = session.query(Vote).get(vote_id)
    if vote:
        session.delete(vote)
        session.commit()