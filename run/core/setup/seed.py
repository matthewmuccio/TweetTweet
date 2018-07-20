#!/usr/bin/env python3


import datetime
import sqlite3


connection = sqlite3.connect("master.db", check_same_thread=False)
cursor = connection.cursor()

username = "admin"
password = "836bc6397d06de5f635683cff01822564683b57c5298c38bd389628685d9ce9d74cba952fc80ac305a6dd1d122bb041dfa93377880d478f27b99da3fafc05bf6"
first_name = "Admin"
last_name = "User"
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

connection.commit()
cursor.close()
connection.close()