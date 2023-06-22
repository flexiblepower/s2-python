
class S2ValidationError(Exception):
    obj: object
    msg: str

    def __init__(self, obj: object, msg, pydantic_validation_error=None):
        self.obj = obj
        self.msg = msg
        self.pydantic_validation_error = pydantic_validation_error
