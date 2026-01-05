"""Base handler for socket server implementations.

This module provides the BaseHandler class which implements common socket server
functionality including connection handling, acknowledgment sending, and message
routing. Subclasses should override _process_message() to implement specific
message handling logic.
"""

import asyncio
from logging import Logger
from typing import TYPE_CHECKING

from src.utils.helpers import construct_script_name
from src.utils.logging_utils import setup_logger

if TYPE_CHECKING:
    from asyncio.streams import StreamReader, StreamWriter

SCRIPT_NAME = construct_script_name(__file__)

MIN_SUGGESTED_PORT = 59000
MAX_SUGGESTED_PORT = 59999


class BaseHandler:
    """Base class for handling socket server messages."""

    port: int
    stop_message: str
    logger: Logger
    stop_event: asyncio.Event

    def __init__(
        self, port: int, stop_message: str, logger: Logger | None = None
    ) -> None:
        """Initialize the BaseHandler."""
        self.port = port
        self.stop_message = stop_message
        self.logger = logger if logger is not None else _assign_default_logger()
        self.stop_event = asyncio.Event()

        self._reader: StreamReader | None = None
        self._writer: StreamWriter | None = None

        if not MIN_SUGGESTED_PORT <= port <= MAX_SUGGESTED_PORT:
            self.logger.warning(f"""port {port} should rather be between
                                {MIN_SUGGESTED_PORT} and {MAX_SUGGESTED_PORT}""")
            print(
                f"Please use a port between {MIN_SUGGESTED_PORT} and {MAX_SUGGESTED_PORT}"  # noqa: E501
            )

    async def _handle_client(self) -> None:
        if self._reader is None or self._writer is None:
            self.logger.error(
                f"Reader or writer is None: reader {self._reader}, writer {self._writer}"  # noqa: E501
            )
            return

        while True:
            data = await self._reader.read(1024)
            if not data:
                self.logger.info("Socket client disconnected")
                break
            message = data.decode()
            await self._handle_message(message)
        self._writer.close()
        await self._writer.wait_closed()

    async def _handle_message(self, message: str) -> None:
        if message == self.stop_message:
            await self._handle_stop_message()
        else:
            await self.process_message(message)

    async def _handle_stop_message(self) -> None:
        self.stop_event.set()
        self.logger.info("Socket received stop message")
        print("Socket received stop message")
        await self._send_ack()

    async def process_message(self, message: str) -> None:
        """Process incoming message using template method pattern.

        Logs the message, sends acknowledgment, then delegates to hook for
        subclass-specific handling.

        Args:
            message: The received message string.

        """
        self.logger.info(f"Socket received: {message}")
        await self._send_ack()
        await self._process_message(message)

    async def _process_message(self, _message: str) -> None:
        """Conduct subclass-specific message processing.

        Override this method in subclasses to implement custom message handling logic.

        Args:
            _message: The received message string to process.

        """

    async def _send_ack(self) -> None:
        if self._writer is None:
            self.logger.error("Writer is None")
            return
        self._writer.write(b"ACK from Socket server")
        await self._writer.drain()

    async def handle_socket_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """Handle new socket client connection.

        Callback method for asyncio.start_server that stores reader/writer
        and initiates client handling.

        Args:
            reader: StreamReader for reading from the client.
            writer: StreamWriter for writing to the client.

        """
        self._reader = reader
        self._writer = writer
        await self._handle_client()

    async def run_socket_server(self) -> None:
        """Run the socket server."""
        self.logger.info("Starting Socket server")
        server = await asyncio.start_server(
            self.handle_socket_client, "localhost", self.port
        )
        addr = server.sockets[0].getsockname()  # pyright: ignore[reportAny]
        self.logger.info(f"Socket server serving on {addr}")

        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            self.logger.exception("Socket server canceled")
        finally:
            server.close()
            await server.wait_closed()
            self.logger.info("Socket server closed")


def _assign_default_logger() -> Logger:
    return setup_logger(SCRIPT_NAME, "DEBUG")
