import datetime
import uuid

from s2wsjson.generated.gen_s2 import Duration, ID


def convert_duration(parsed_duration: Duration) -> datetime.timedelta:
    return datetime.timedelta(milliseconds=parsed_duration.value)


def convert_id(parsed_id: ID) -> uuid.UUID:
    return uuid.UUID(parsed_id.value)
