class InternalServerError(Exception):
    def __init__(self, message):
        self.message = message
        super(InternalServerError, self).__init__(message)

class ClientError(Exception):
    def __init__(self, message):
        self.message = message
        super(ClientError, self).__init__(message)

class TooManyRequests(Exception):
    def __init__(self, message):
        self.message = message
        super(TooManyRequests, self).__init__(message)

class RetryLimitExceeded(Exception):
    def __init__(self, message):
        self.message = message
        super(RetryLimitExceeded, self).__init__(message)
