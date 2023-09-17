""" API for testing purposes"""
from flask import Flask, request

from ticket_bucket import TicketBucket


app = Flask(__name__)

register = {}

rate_limiter = TicketBucket


@app.before_request
def throttler():
    """Limits the rate of request to routes"""
    if request.url_rule.rule == "/limited":
        address = request.remote_addr
        if address in register:
            if not register[address].allow_request():
                return "Too much requests", 429
        else:
            register[address] = rate_limiter(10, 1)


@app.route("/limited", strict_slashes=False)
def limited():
    """A limited endpoint"""
    return "Limited, don't over use me!"


@app.route("/unlimited", strict_slashes=False)
def unlimited():
    """An Unlimited endpoint"""
    return "Unlimited! Let's Go!"
