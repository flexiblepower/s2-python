import asyncio
import websockets
import logging
import json
import uuid
from datetime import datetime, timezone

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mock_s2_websocket")

# WebSocket server port
WS_PORT = 8080


# Handle client connection
async def handle_connection(
    websocket: websockets.WebSocketServerProtocol, path: str
) -> None:
    client_id = str(uuid.uuid4())
    logger.info(f"Client {client_id} connected on path: {path}")

    try:
        # Send handshake message to client
        handshake = {
            "type": "Handshake",
            "messageId": str(uuid.uuid4()),
            "protocolVersion": "0.0.2-beta",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        await websocket.send(json.dumps(handshake))
        logger.info(f"Sent handshake to client {client_id}")

        # Listen for messages
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.info(f"Received message from client {client_id}: {data}")

                # Extract message type
                message_type = data.get("type", "")
                message_id = data.get("messageId", str(uuid.uuid4()))

                # Send reception status
                reception_status = {
                    "type": "ReceptionStatus",
                    "messageId": str(uuid.uuid4()),
                    "refMessageId": message_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "OK",
                }
                await websocket.send(json.dumps(reception_status))
                logger.info(f"Sent reception status for message {message_id}")

                # Handle specific message types
                if message_type == "HandshakeResponse":
                    logger.info("Received handshake response")

                # For FRBC messages, you could add specific handling here

            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from client {client_id}")
            except Exception as e:
                logger.error(f"Error processing message from client {client_id}: {e}")

    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Connection with client {client_id} closed")
    except Exception as e:
        logger.error(f"Error with client {client_id}: {e}")
    finally:
        logger.info(f"Client {client_id} disconnected")


async def start_server() -> None:
    server = await websockets.serve(handle_connection, "localhost", WS_PORT)
    logger.info(f"WebSocket server started on ws://localhost:{WS_PORT}")

    # Keep the server running
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(start_server())
