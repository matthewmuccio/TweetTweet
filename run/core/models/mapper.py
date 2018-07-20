#!/usr/bin/env python3


import datetime
import hashlib
import re
import sqlite3

#import pandas as pd


# Encrypt a plaintext string (password) with SHA-512 cryptographic hash function.
def encrypt_password(password):
	return hashlib.sha512(str.encode(password)).hexdigest()

# Creates an account in users database table.
def create_account(username, password, first_name, last_name):
	if not valid_name(first_name, last_name):
		return ["Sorry, names can only contain letters, apostrophes, or hyphens.", "They must contain between 1 and 50 characters."]
	if account_exists(username, password):
		return ["Sorry, an account with that username and password already exists.", "Log in with those credentials to access your account."]
	elif username_exists(username):
		return ["Sorry, the username you entered is already taken."]
	elif not valid_username(username):
		return ["Sorry, the username you entered is invalid.", "Usernames must contain between 3 and 20 characters.", "They can only contain lowercase letters, numbers, and underscores."]
	elif not valid_password(password):
		return ["Sorry, the password you entered is invalid.", "Passwords must contain between 8 and 50 characters."]
	username = username.lower()
	first_name = first_name.lower().capitalize()
	last_name = last_name.lower().capitalize()
	password = encrypt_password(password)
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	num_posts = 0
	num_reposts = 0
	first_login = datetime.datetime.now().replace(microsecond=0)
	last_login = first_login

	cursor.execute(
		"""INSERT INTO users(
			username,
			password,
			first_name,
			last_name,
			num_posts,
			num_reposts,
			first_login,
			last_login
		) VALUES(?,?,?,?,?,?,?,?);""", (username, password, first_name, last_name, num_posts, num_reposts, first_login, last_login,)
	)
	return ["Success", "User"]

# Logs in to account in users database table.
def login(username, password):
	if not username_exists(username):
		return ["Sorry, no account exists with that username.", "Please sign up for a Web Trader account to log in."]
	elif not account_exists(username, password):
		return ["Sorry, the password you entered was incorrect."]
	elif is_admin(username, password):
		update_last_login(username)
		return ["Success", "Admin"]
	password = encrypt_password(password)
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	if result:
		# Updates last_login in users database table.
		update_last_login(username)
		return ["Success", "User"]

# Checks if an account (username and password) is the admin account.
def is_admin(username, password):
	return username == "admin" and account_exists(username, password)

# Checks if a username is valid.
def valid_username(username):
	return re.search(r"\A[a-z0-9_]{3,20}\Z", username)
 
# Checks if a password is valid.
def valid_password(password):
	regex = r"\A[A-Za-z0-9\"\^\-\]\\~`!@#$%&*()_+=|{}[:;'<>,.?/]{8,50}\Z"
	return re.search(regex, password)

# Checks if a first and last name are valid.
def valid_name(first_name, last_name):
	regex = r"\A[A-Za-z\-']{1,50}\Z"
	return re.search(regex, first_name) and re.search(regex, last_name)

### SELECT (GET)

# Checks if a username exists in a row in the users database table.
def username_exists(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=?", (username,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return result

# Checks if an account (username and password) exists in a row in the users database table.
def account_exists(username, password):
	password = encrypt_password(password)
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return result

# Returns the user's first and last name in a tuple, or None if username does not exist.
def get_name(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT first_name, last_name FROM users WHERE username=?", (username,))
	try:
		result = cursor.fetchall()[0]
	except IndexError:
		result = None
	cursor.close()
	connection.close()
	return result

### UPDATE / INSERT
# Updates the last login time in the users database table to the current time (when the uesr logs in).
def update_last_login(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("UPDATE users SET last_login=? WHERE username=?", (datetime.datetime.now().replace(microsecond=0), username,))
	connection.commit()
	cursor.close()
	connection.close()