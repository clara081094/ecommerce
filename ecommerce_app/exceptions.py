from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class ExceptionParams(APIException):
    status_code = 400
    default_detail = "Data sent is invalid"
    default_code = "ERROR"

    def __init__(self, status_code=None, message=None, errors=None):

        errors = [] if errors is None else errors
        self.status_code = status_code if status_code else self.status_code
        self.detail = {
            "code": self.status_code,
            "message": message if message else self.default_detail,
            "errors": [{x: errors[x]} for x in errors.keys()]
            if type(errors) == dict
            else errors,
        }


def custom_exception_handler(exec, context):

    response = exception_handler(exec, context)

    if response and response.status_code == 403:
        response.data = {
            "code": "AUTHENTICATION ERROR",
            "message": "Not authenticated",
            "errors": ["Authentication credentias were not provided"],
        }
    

    return response