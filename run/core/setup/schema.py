#!/usr/bin/env python3


import sqlite3


connection = sqlite3.connect("master.db", check_same_thread=False)
cursor = connection.cursor()

# Creates users table.
cursor.execute(
	"""CREATE TABLE users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(20) UNIQUE NOT NULL,
		password VARCHAR(128) NOT NULL,
		first_name VARCHAR(50) NOT NULL,
		last_name VARCHAR(50) NOT NULL,
		num_posts INTEGER NOT NULL,
		num_reposts INTEGER NOT NULL,
		first_login DATETIME NOT NULL,
		last_login DATETIME NOT NULL
	);"""
)

# Creates posts table.
cursor.execute(
	"""CREATE TABLE posts(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		author_username VARCHAR(20) NOT NULL,
		author_first_name VARCHAR(50) NOT NULL,
		author_last_name VARCHAR(50) NOT NULL,
		content VARCHAR(280) NOT NULL,
		post_time DATETIME NOT NULL,
		FOREIGN KEY(author_username) REFERENCES users(username),
		FOREIGN KEY(author_first_name) REFERENCES users(first_name),
		FOREIGN KEY(author_last_name) REFERENCES users(last_name)
	);"""
)

# Creates reposts table.
cursor.execute(
	"""CREATE TABLE reposts(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		reposter_username VARCHAR(20) NOT NULL,
		post_id INTEGER NOT NULL,
		FOREIGN KEY(reposter_username) REFERENCES users(username),
		FOREIGN KEY(post_id) REFERENCES posts(id)
	);"""
)

cursor.close()
connection.close()