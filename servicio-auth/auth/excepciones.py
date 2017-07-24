

class BaseError(Exception):
    code = "0000"
    status = 500

    def __init__(self, message, code=None, status=None):
        self.message = message
        if code is not None:
            self.code = code
        if status is not None:
            self.status = status

    def getJSON(self):
        return {"codigo": self.code, "mensaje": self.message}


class DatabaseError(BaseError):
    code = "0001"


class AuthError(BaseError):
    code = "0002"
    status = 401


class CamposInvalidosError(BaseError):
    code = "0003"
    status = 400


class RefreshTokenError(BaseError):
    code = "0004"
    status = 400
