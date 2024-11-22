from flask import Blueprint


sample = Blueprint(
    "sample", __name__)


def page():
    return "Hello, sample!"


sample.add_url_rule(
    "/sample/page", view_func=page)


def get_blueprints():
    return [sample]
