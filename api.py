""" API for testing purposes"""
from os import getenv
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

from ticket_bucket import TicketBucket
from fixed_win_counter import FixedWindowCounter


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

register = {}

# Using Ticket Bucket Algorithm
rate_limiter = TicketBucket

# # Using Fixed Window Algorithm
# rate_limiter = FixedWindowCounter


@app.before_request
def throttler():
    """Limits the rate of request to routes"""
    rule = request.url_rule
    if rule and (rule.rule == "/limited"):
        address = getenv("X-Forwarded-For")
        if not address:
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
