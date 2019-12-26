RESPONSE_CODES = {
    200: "200 OK",
    400: "400 Bad Request",
    404: "404 Not Found",
    500: "500 Internal Server Error"
    }


class Response:
    def __init__(self, response_code, data, content_type="text/html"):
        self.content_type = content_type
        self.data = data
        self._payload = f"""HTTP/1.1 {RESPONSE_CODES[response_code]}\n"""
        self._payload+= f"""Content-Type: {content_type};charset=UTF-8\n"""
        try:
            self._payload+= f"""Content-Length: {len(data.encode('utf-8'))}\n\n"""
        except AttributeError:
            self._payload+= f"""Content-Length: {len(data)}\n\n"""

    def serialize(self):
        if self.content_type in ["image/webp", "image/gif"]:
            payload = bytes(self._payload, "utf-8")
            if isinstance(self.data, bytes):
                payload += self.data
            else:
                payload += bytes(self.data, 'utf-8')
        else:
            payload = self._payload + self.data
            payload = bytes(payload, 'utf-8')
        return payload
