#!/usr/bin/env python3


from flask import Blueprint, render_template


controller = Blueprint("featured", __name__)


@controller.route("/")
def home():
	return render_template("index.html")
