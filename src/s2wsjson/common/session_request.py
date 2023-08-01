from s2wsjson.generated.gen_s2 import SessionRequest as GenSessionRequest
from s2wsjson.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class SessionRequest(GenSessionRequest, ValidateValuesMixin['SessionRequest']):
    class Config(GenSessionRequest.Config):
        validate_assignment = True

    message_id: uuid.UUID = SessionRequest.__fields__['message_id'].field_info  # type: ignore[assignment]