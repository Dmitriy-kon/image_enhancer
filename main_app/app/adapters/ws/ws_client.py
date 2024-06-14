from fastapi import WebSocket


class WebSocketClient:
    def __init__(self):
        self.webscockets: dict[str, WebSocket] = {}

    def add_file(self, filename: str, ws: WebSocket):
        self.webscockets[filename] = ws

    def remove_file(self, filename: str):
        self.webscockets.pop(filename, None)

    def get_file(self, filename: str) -> WebSocket:
        return self.webscockets.get(filename)


webscocket_client = WebSocketClient()

__all__ = ["webscocket_client"]
