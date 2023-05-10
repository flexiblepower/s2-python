
class S2ValidationError(Exception):
    obj: object
    msg: str

    def __init__(self, obj: object, msg):
        self.obj = obj
        self.msg = msg
