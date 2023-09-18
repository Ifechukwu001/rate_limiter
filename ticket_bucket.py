"""Ticket Bucket class"""
from datetime import datetime


class TicketBucket:

    def __init__(self, max_size: int, refill_size: int):
        """Constructor for the TicketBucket"""
        self.max_size = max_size
        self.refill_size = refill_size

        self.current_size = self._max_size
        self.lastrefill = datetime.utcnow()

    @property
    def max_size(self):
        """Returns the max_size"""
        return self._max_size

    @max_size.setter
    def max_size(self, value: int):
        """Sets the max_size value"""
        if type(value) is not int:
            raise TypeError("max_size is not an int")
        self._max_size = value

    @property
    def refill_size(self):
        """Returns the refill_size"""
        return self._refill_size

    @refill_size.setter
    def refill_size(self, value: int):
        """Sets the refill_size value"""
        if type(value) is not int:
            raise TypeError("refill_size is not an int")
        self._refill_size = value

    def allow_request(self):
        """Checks if to allow a request"""
        self.refill_bucket()

        if self.current_size:
            self.current_size -= 1
            return True
        return False

    def refill_bucket(self):
        """Refills the token bucket"""
        now = datetime.utcnow()
        time_diff = now - self.lastrefill
        token = time_diff * self.refill_size
        token = token.seconds

        self.current_size = token if token <= self.max_size else self.max_size
