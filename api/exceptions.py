from rest_framework.exceptions import APIException

class PaginationException(APIException):
    def __init__(self, detail=None):
        super().__init__(detail=detail)
        self.status_code = 400

class UnauthorizedUserGroupException(APIException):
    def __init__(self, detail=None):
        super().__init__(detail=detail)
        self.status_code = 403

class InvalidUserTypeException(APIException):
    def __init__(self, detail=None):
        super().__init__(detail=detail)
        self.status_code = 400

class BadRequestException(APIException):
    def __init__(self, detail=None):
        super().__init__(detail=detail)
        self.status_code = 400