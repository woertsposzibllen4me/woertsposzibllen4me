"""Constants related to connections and subprocesses."""

STREAMERBOT_WS_URL = "ws://127.0.0.1:50001/"
"""Defined in the Streamer.bot application settings."""

STOP_SUBPROCESS_MESSAGE = "stop$subprocess"
"""Message sent to the subprocess's socket handler to signal it to stop running. The `$`
character is used as a marker to avoid accidental triggering from speech-to-text
transcription."""

SUBPROCESSES_PORTS = {
    "shopwatcher": 59000,
    "pregamespy": 59001,
    "robeau": 59002,
    "synonym_adder": 59003,
}
"""Mapping of subprocess names to their respective port numbers."""
