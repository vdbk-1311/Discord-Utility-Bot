from flask import Blueprint, redirect, request
from .oauth import get_token

routes = Blueprint("routes", __name__)

@routes.route("/login")

def login():

    return redirect(
        "https://discord.com/oauth2/authorize"
    )

@routes.route("/callback")

def callback():

    code = request.args.get("code")

    token = get_token(code)

    return token