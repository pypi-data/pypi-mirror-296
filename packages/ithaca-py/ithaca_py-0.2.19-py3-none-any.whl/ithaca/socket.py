"""Socket Module."""

import ssl
import time
from json import dumps, loads
from logger import logger

import websocket


class Socket:
    """Socket Class."""

    def __init__(self, parent):
        """Class constructor."""
        self.parent = parent
        self._ws_app = None
        self.reconnect_delay = 5

    def __on_open(self, ws):
        logger.info("Socket connection open...")
        params = {
            "action": "VALIDATE_AUTH_TOKEN",
            "payload": self.parent.user.get("authToken"),
        }
        ws.send(dumps(params))

    def __on_error(self, ws, error):
        logger.error(f"Socket error: {error}")

    def __on_close(self, ws, close_status_code, close_msg):
        logger.warning("Socket closed. Status code:", close_status_code, "Message:", close_msg)
        self._attempt_reconnect()

    def __on_message(self, ws, message):
        data = loads(message)
        if data.get("responseType") == "EXEC_REPORT":
            payload = data.get("payload")
            logger.debug(payload)
        else:
            logger.debug(data)

    def _attempt_reconnect(self):
        """Attempt to reconnect after a fixed delay."""
        logger.info(f"Reconnecting in {self.reconnect_delay} seconds...")
        time.sleep(self.reconnect_delay)
        self.parent.auth.login_rsa()
        self.connect()

    def connect(self, on_message=None):
        """Attempt to connect to the WebSocket endpoint."""
        logger.info(f"Attempting to connect to WebSocket at {self.parent.ws_url}...")
        logger.debug(f"Using auth token: {self.parent.user.get('authToken')}")

        if on_message is None:
            on_message = self.__on_message

        self._ws_app = websocket.WebSocketApp(
            url=self.parent.ws_url,
            on_message=on_message,
            on_error=self.__on_error,
            on_close=self.__on_close,
            on_open=self.__on_open,
        )
        sslopt = (
            {"cert_reqs": ssl.CERT_NONE}
            if "localhost" in self.parent.base_url
            else None
        )

        # Attempt to run the WebSocket client
        try:
            self._ws_app.run_forever(ping_interval=14, sslopt=sslopt)
        except Exception as e:
            logger.error(f"Exception in WebSocket: {e}")
            self._attempt_reconnect()

    def close(self):
        """Manually close the WebSocket connection."""
        if self._ws_app:
            self._ws_app.close()
            logger.info("WebSocket connection closed manually.")
