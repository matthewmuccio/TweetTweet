#!/usr/bin/env python3


import collections
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
	num_posts = 0
	num_reposts = 0
	first_login = datetime.datetime.now().replace(microsecond=0)
	last_login = first_login

	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
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
	connection.commit()
	cursor.close()
	connection.close()
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

# Returns the number of posts of a given username.
def get_num_posts(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT num_posts FROM users WHERE username=?", (username,))
	try:
		result = cursor.fetchall()[0][0]
	except IndexError:
		result = None
	cursor.close()
	connection.close()
	return result

# Returns the number of reposts of a given username.
def get_num_reposts(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT num_reposts FROM users WHERE username=?", (username,))
	try:
		result = cursor.fetchall()[0][0]
	except IndexError:
		result = None
	cursor.close()
	connection.close()
	return result

# Returns all the posts and post times for a given username.
def get_posts(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT id, content, post_time FROM posts WHERE author_username=? ORDER BY post_time DESC", (username,))
	try:
		result = cursor.fetchall()
		print(result)
		posts = {}
		for r in result:
			posts[r[0]] = [r[1], r[2]]
		all_posts = collections.OrderedDict(sorted(posts.items(), reverse=True))
	except (TypeError, IndexError):
		return None
	cursor.close()
	connection.close()
	return all_posts

# Returns all the posts and post times in the database.
def get_all_posts():
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT id, author_username, author_first_name, author_last_name, content, post_time FROM posts ORDER BY post_time DESC")
	try:
		result = cursor.fetchall()
		posts = {}
		for r in result:
			posts[r[0]] = [r[1], r[2], r[3], r[4], r[5]]
		all_posts = collections.OrderedDict(sorted(posts.items(), reverse=True))
	except (TypeError, IndexError):
		return None
	cursor.close()
	connection.close()
	return all_posts

# Retrieves a post and its information by its id.
def get_post(post_id):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT id, author_username, author_first_name, author_last_name, content, post_time FROM posts WHERE id=? ORDER BY post_time DESC", (post_id,))
	try:
		result = cursor.fetchall()
		for r in result:
			post = [r[1], r[2], r[3], r[4], r[5]]
	except (TypeError, IndexError):
		return None
	cursor.close()
	connection.close()
	return post

# Returns all the reposts for a given username.
def get_reposts(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT post_id FROM reposts WHERE reposter_username=?", (username,))
	try:
		post_ids = cursor.fetchall()
		post_ids_list = [i[0] for i in post_ids]
	except (TypeError, IndexError):
		return None
	reposts = {}
	for post_id in post_ids_list:
		reposts[post_id] = get_post(post_id)
	cursor.close()
	connection.close()
	return reposts

### UPDATE / INSERT
# Adds a new post to the posts database table.
def add_new_post(username, content):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	first_name, last_name = get_name(username)
	post_time = datetime.datetime.now().replace(microsecond=0)
	update_num_posts(username)
	cursor.execute("""INSERT INTO posts(
						author_username,
						author_first_name,
						author_last_name,
						content,
						post_time) VALUES(?,?,?,?,?);""", (username, first_name, last_name, content, post_time,))
	connection.commit()
	cursor.close()
	connection.close()

# Adds a new repost to the posts database table.
def add_new_repost(username, post_id):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	update_num_reposts(username)
	cursor.execute("""INSERT INTO reposts(
						post_id,
						reposter_username) VALUES(?,?);""", (post_id, username,))
	connection.commit()
	cursor.close()
	connection.close()

# Updates the last login time in the users database table to the current time (when the uesr logs in).
def update_last_login(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("UPDATE users SET last_login=? WHERE username=?", (datetime.datetime.now().replace(microsecond=0), username,))
	connection.commit()
	cursor.close()
	connection.close()

# Updates the user's number of posts, as they just added a post.
def update_num_posts(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	num_posts = get_num_posts(username)
	cursor.execute("UPDATE users SET num_posts=? WHERE username=?", (num_posts + 1, username,))
	connection.commit()
	cursor.close()
	connection.close()

# Updates the user's number of posts, as they just added a post.
def update_num_reposts(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	num_reposts = get_num_reposts(username)
	cursor.execute("UPDATE users SET num_reposts=? WHERE username=?", (num_reposts + 1, username,))
	connection.commit()
	cursor.close()
	connection.close()