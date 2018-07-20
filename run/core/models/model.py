#!/usr/bin/env python3


from core.models import mapper
from core.models import wrapper


# Creates an account in users database table.
def create_account(username, password, first_name, last_name):
	return mapper.create_account(username, password, first_name, last_name)

# Logs in to account in users database table.
def login(username, password):
	return mapper.login(username, password)

# Returns the user's first and last name in a tuple.
def get_name(username):
	return mapper.get_name(username)