#!/usr/bin/env python

import asyncio
import websockets
import uuid
from s2python.common import EnergyManagementRole, Handshake, ReceptionStatus, ReceptionStatusValues
import json

async def hello():
    """
    Connects to a WebSocket server, sends a message,
    and prints the response.
    """
    uri = "ws://localhost:8080"  # <-- Replace with your server's URI
    try:
        async with websockets.connect(uri) as websocket:
            message = Handshake(
                message_id=uuid.uuid4(),
                role=EnergyManagementRole.RM,
                supported_protocol_versions=["1.0"],
            )

            await websocket.send(message.to_json())
            print(f">>> {message.to_json()}")

            reception_status = await websocket.recv()
            reception_status_json = json.loads(reception_status)
            print(f"<<< {reception_status_json}")

            handshake_response = await websocket.recv()
            handshake_response_json = json.loads(handshake_response)
            print(f"<<< {handshake_response_json}")

            reception_status = ReceptionStatus(
                subject_message_id=handshake_response_json["message_id"],
                status=ReceptionStatusValues.OK,
                diagnostic_label="Handshake received",
            )
            await websocket.send(reception_status.to_json())
            print(f">>> {reception_status.to_json()}")
            response = await websocket.recv()
            
            print(f"<<< {response}")

    except ConnectionRefusedError:
        print(f"Connection to {uri} refused. Is the server running?")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(hello())
