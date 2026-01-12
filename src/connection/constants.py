"""Constants related to connections and subprocesses."""

STREAMERBOT_WS_URL = "ws://127.0.0.1:50001/"  # Defined in the Streamer.bot app settings

STOP_SUBPROCESS_MESSAGE = "stop$subprocess"  # $ character is used to avoid accidental
# trigger from speech to text.

SUBPROCESSES_PORTS = {  # subprocesses socket server ports
    "shopwatcher": 59000,
    "pregamespy": 59001,
    "robeau": 59002,
    "synonym_adder": 59003,
}
