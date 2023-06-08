from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("Default", "default", description="Default operation for diagnosis.")

@blp.route("/flask-health-check")
class BaseHealthCehck(MethodView):
    def get(self):
        return "success"
    