#!/usr/bin/env python3


from flask import abort, Blueprint, redirect, render_template, request, session, url_for

from core.models import model


controller = Blueprint("profile", __name__, url_prefix="/profile")

@controller.route("/", methods=["GET"])
def show_profile():
    return render_template("profile.html")