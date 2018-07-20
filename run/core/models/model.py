#!/usr/bin/env python3


from core.models import mapper
from core.models import wrapper


# Creates an account in users database table.
def create_account(username, password, first_name, last_name):
	return mapper.create_account(username, password, first_name, last_name)

# Logs in to account in users database table.
def login(username, password):
	return mapper.login(username, password)

# Adds a new post to the posts database table.
def add_new_post(username, content):
	return mapper.add_new_post(username, content)

# Adds a new repost to the posts database table.
def add_new_repost(username, post_id):
	return mapper.add_new_repost(username, post_id)

# Returns the user's first and last name in a tuple.
def get_name(username):
	return mapper.get_name(username)

# Returns the number of posts of a given username.
def get_num_posts(username):
	return mapper.get_num_posts(username)

# Returns the number of reposts of a given username.
def get_num_reposts(username):
	return mapper.get_num_reposts(username)

# Returns all the posts for a given username.
def get_posts(username):
	return mapper.get_posts(username)

def get_reposts(username):
	return mapper.get_reposts(username)

# Returns all the posts and post times in the database.
def get_all_posts():
	return mapper.get_all_posts()