# A file to keep track of all the tools needed to modify/update the databse

import json

database_dict = {}

# opens databse
try:
    with open('user_data.json', 'r') as user_data:
        database_dict = json.load(user_data)
except json.decoder.JSONDecodeError:
    database_dict = {}
    
def user_exists(username):
    """
    Checks if a user is currently in the databse via binary search
    """
    return username in database_dict
    
    
def add_user(username):
    """
    Adds user to database
    """
    database_dict[username] = 0
    
    
def get_highscore(username):
    """
    Retrieves the highscore of the user
    """
    return database_dict[username]
    
    
def update_highscore(username, highscore):
    """
    Updates the highscore of a user
    """
    database_dict[username] = highscore
    

def upload_user_data():
    """
    Uploads the updated database
    """
    global database_dict
    database_dict = dict(sorted(database_dict.items()))
    with open('user_data.json', 'w') as user_data:
        json.dump(database_dict, user_data, indent=4)