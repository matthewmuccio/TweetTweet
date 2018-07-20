#!/usr/bin/env python3


from flask import Blueprint, redirect, render_template, request, session, url_for

from core.models import model


controller = Blueprint("login", __name__, url_prefix="/login")

@controller.route("/", methods=["GET", "POST"])
def show_login():
	# In session (user signed in)
	if "username" in session:
		return redirect(url_for("main.show_main"))
	# Out of session (user not signed in)
	else:
		# GET request
		if request.method == "GET":
			return render_template("login.html")
		# POST request
		else:
			# Accesses current form data (data transmitted in a POST request).
			username = request.form["username"]
			password = request.form["password"]
			# Attempts to log in to the account with the entered username and password.
			response = model.login(username, password)
			# If the user has successfully logged in to their account.
			if "Success" in response:
				session["username"] = username
				session["first_name"], session["last_name"] = model.get_name(username)
				# If it is the admin user.
				if "Admin" in response:
					# TODO: Add admin functionality.
					return redirect(url_for("main.show_main"))
				# If it is any other user.
				else:
					return redirect(url_for("main.show_main"))
			# If there was an issue with logging in to the account (username or account does not exist).
			else:
				return render_template("login.html", response=response)