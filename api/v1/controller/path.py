from flask import Blueprint
app_controller = Blueprint("app_controller", __name__, url_prefix="/api/v1")

from api.v1.controller.index import *
from api.v1.controller.users import *
from api.v1.controller.posts import *
from api.v1.controller.tags import *
