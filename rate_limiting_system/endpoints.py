from flask import Blueprint, jsonify
from rate_limiting_system.rate_limiter import rate_limiter
from os import environ

main = Blueprint("main", __name__)


@main.route("/")
@rate_limiter(
    max_tokens=int(environ.get("MAX_TOKENS", 2)),
    seconds_per_token=int(environ.get("SECONDS_PER_TOKEN", 10))
)
def hello_world():
    return jsonify(message="Hello World"), 200
