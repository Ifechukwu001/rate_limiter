"""Fixed Window Counter class"""
from datetime import datetime


class FixedWindowCounter:

    def __init__(self, max_request: int, time_window: int):
        """Initializes the max_request and time_window"""
        self.max_request = max_request
        self.time_window = time_window

        self.initial_time = datetime.utcnow()
        self.request_count = 0

    @property
    def max_request(self):
        """Maximum requests allowed"""
        return self._max_request

    @max_request.setter
    def max_request(self, value):
        if type(value) is not int:
            raise TypeError("max_request must be an int")
        self._max_request = value

    @property
    def time_window(self):
        """Max window time for max requests"""
        return self._time_window

    @time_window.setter
    def time_window(self, value):
        if type(value) is not int:
            raise TypeError("time_window must be an int")
        self._time_window = value

    def allow_request(self):
        """Checks if a request is permitted"""
        if self.within_interval() and self.much_requests():
            return False
        return True

    def within_interval(self):
        """Checks the interval of the request"""
        now = datetime.utcnow()
        interval = now - self.initial_time
        interval = interval.seconds

        if interval >= self.time_window:
            self.initial_time = now
            self.request_count = 0
        return True

    def much_requests(self):
        """Checks if request has exceeded limit"""
        if self.request_count > self.max_request:
            return True
        return False
