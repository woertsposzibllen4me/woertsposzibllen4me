"""WebSocket client for sending and receiving JSON messages with external apps."""

from logging import Logger
from typing import final

import aiofiles
import websockets
from websockets import (
    ClientConnection,
    ConnectionClosedError,
    WebSocketException,
)

from src.utils.helpers import construct_script_name
from src.utils.logging_utils import setup_logger

SCRIPT_NAME = construct_script_name(__file__)


@final
class WebSocketClient:
    """WebSocket client for sending and receiving JSON messages."""

    def __init__(self, url: str, logger: Logger | None = None) -> None:
        """Initialize the WebSocketClient."""
        self.url = url
        self.logger = logger if logger else self._assign_default_logger()
        self.ws: ClientConnection | None = None

    async def establish_connection(
        self,
    ) -> ClientConnection | None:
        """Establish a websocket connection."""
        self.logger.info("Establishing websocket connection")
        try:
            self.ws = await websockets.connect(self.url)
            self.logger.info(f"Established websocket connection: {self.ws}")
        except ConnectionRefusedError as e:
            self.logger.error(f"Connection refused: {e}")  # noqa: TRY400 # No need to
            # vomit in the logs for a simple case of not running the websocket server
            # this connects to..
        except WebSocketException:
            self.logger.exception("Websocket Exception")
        except OSError:
            self.logger.exception("Websocket error")
        return self.ws

    async def send_json_requests(self, json_file_paths: list[str] | str) -> None:
        """Send JSON requests from file(s) over the websocket connection."""
        if isinstance(json_file_paths, str):
            json_file_paths = [json_file_paths]

        if not self.ws:
            self.logger.warning("No websocket connection established")
            return

        for json_file in json_file_paths:
            try:
                async with aiofiles.open(json_file) as file:
                    content = await file.read()
                    await self.ws.send(content)

                response = await self.ws.recv()
                if isinstance(response, bytes):
                    response = response.decode("utf-8")
                self.logger.info(f"WebSocket response: {response}")

            except ConnectionClosedError:
                self.logger.exception("WebSocket connection closed")
            except FileNotFoundError:
                self.logger.exception(f"file not found: {json_file}")
            except WebSocketException:
                self.logger.exception("WebSocket error")
            except Exception:
                self.logger.exception("Unexpected error while sending JSON request")

    async def close(self) -> None:
        """Close the websocket connection."""
        if self.ws:
            await self.ws.close()
            self.logger.info("WebSocket connection closed")

    @staticmethod
    def _assign_default_logger() -> Logger:
        return setup_logger(SCRIPT_NAME)
