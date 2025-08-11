import json
import unittest
import datetime
import uuid

from s2python.validate_values_mixin import S2MessageComponent


class MockS2Message(S2MessageComponent):
    some_uuid: uuid.UUID
    some_str: str
    some_float: float
    some_datetime: datetime.datetime
    some_timedelta: datetime.timedelta


def example_message() -> MockS2Message:
    return MockS2Message(some_uuid=uuid.uuid4(),
                         some_str='asdaa',
                         some_float=3.14,
                         some_datetime=datetime.datetime.now(),
                         some_timedelta=datetime.timedelta(hours=1, minutes=1))


class TestS2MessageComponent(unittest.TestCase):
    def test__to_json__okay(self):
        # Arrange
        message = example_message()

        # Act
        json_str = message.to_json()

        # Assert
        message_json = json.loads(json_str)
        self.assertEqual(message_json['some_uuid'], str(message.some_uuid))
        self.assertEqual(message_json['some_str'], message.some_str)
        self.assertEqual(message_json['some_float'], message.some_float)
        self.assertEqual(message_json['some_datetime'], message.some_datetime.isoformat())
        self.assertEqual(message_json['some_timedelta'], 'PT1H1M')

    def test__to_dict__okay(self):
        # Arrange
        message = example_message()

        # Act
        message_dict = message.to_dict()

        # Assert
        self.assertEqual(message_dict['some_uuid'], message.some_uuid)
        self.assertEqual(message_dict['some_str'], message.some_str)
        self.assertEqual(message_dict['some_float'], message.some_float)
        self.assertEqual(message_dict['some_datetime'], message.some_datetime)
        self.assertEqual(message_dict['some_timedelta'], message.some_timedelta)

    def test__to_json_dict__okay(self):
        # Arrange
        message = example_message()

        # Act
        message_dict = message.to_json_dict()

        # Assert
        json.dumps(message_dict)
        self.assertEqual(message_dict['some_uuid'], str(message.some_uuid))
        self.assertEqual(message_dict['some_str'], message.some_str)
        self.assertEqual(message_dict['some_float'], message.some_float)
        self.assertEqual(message_dict['some_datetime'], message.some_datetime.isoformat())
        self.assertEqual(message_dict['some_timedelta'], 'PT1H1M')
