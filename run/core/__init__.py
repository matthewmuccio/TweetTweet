#!/usr/bin/env python3


from flask import Flask

from core.controllers.featured import controller as featured


omnibus = Flask(__name__)

omnibus.register_blueprint(featured)
