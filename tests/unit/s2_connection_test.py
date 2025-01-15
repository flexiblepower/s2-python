# import unittest
#
#
# class S2ConnectionTest(unittest.TestCase):
#     async def test__send_and_await_reception_status__receive_while_waiting(self):
#         # Arrange
#         conn = Mock()
#         awaiter = ReceptionStatusAwaiter()
#         message_id = "1"
#         s2_message = {
#             "message_type": "Handshake",
#             "message_id": message_id,
#             "role": "RM",
#             "supported_protocol_versions": ["1.0"],
#         }
#         s2_reception_status = {
#             "message_type": "ReceptionStatus",
#             "subject_message_id": message_id,
#             "status": "OK",
#         }
#
#         # Act
#         wait_task = asyncio.create_task(
#             awaiter.send_and_await_reception_status(conn, s2_message, True)
#         )
#         should_be_waiting_still = not wait_task.done()
#         await awaiter.receive_reception_status(s2_reception_status)
#         await wait_task
#         received_s2_reception_status = wait_task.result()
#
#         # Assert
#         expected_s2_reception_status = {
#             "message_type": "ReceptionStatus",
#             "subject_message_id": "1",
#             "status": "OK",
#         }
#
#         self.assertTrue(should_be_waiting_still)
#         self.assertEqual(expected_s2_reception_status, received_s2_reception_status)
#
#     async def test__send_and_await_reception_status__receive_while_waiting_not_okay(self):
#         # Arrange
#         conn = Mock()
#         awaiter = ReceptionStatusAwaiter()
#         message_id = "1"
#         s2_message = {
#             "message_type": "Handshake",
#             "message_id": message_id,
#             "role": "RM",
#             "supported_protocol_versions": ["1.0"],
#         }
#         s2_reception_status = {
#             "message_type": "ReceptionStatus",
#             "subject_message_id": message_id,
#             "status": "INVALID_MESSAGE",
#         }
#
#         # Act / Assert
#         wait_task = asyncio.create_task(
#             awaiter.send_and_await_reception_status(conn, s2_message, True)
#         )
#         await awaiter.receive_reception_status(s2_reception_status)
#
#         with self.assertRaises(RuntimeError):
#             await wait_task
