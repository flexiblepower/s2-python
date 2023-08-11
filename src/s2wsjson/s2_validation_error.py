from pydantic import ValidationError

class S2ValidationError(Exception):
    obj: object
    msg: str
    pydantic_validation_error: 'ValidationError | TypeError | None'

    def __init__(self, obj: object, msg: str, pydantic_validation_error: 'ValidationError | TypeError | None' = None):
        self.obj = obj
        self.msg = msg
        self.pydantic_validation_error = pydantic_validation_error
