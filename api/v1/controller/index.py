#!/usr/bin/python3
"""stat"""
#from api.v1.views import app_views
from flask import jsonify
from flask import Blueprint
from api.v1.controller.path import app_controller

@app_controller.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Status me the status of my application"""
    return jsonify({"status": "OK"})
