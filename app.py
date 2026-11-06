import base64
import binascii
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import ddddocr

ocr = ddddocr.DdddOcr(show_ad=False)


class Handler(BaseHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        self.send_error_text(message or "请求处理失败")

    def send_error_text(self, message):
        body = message.encode("utf-8")
        self.send_response(500)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/health":
            self.send_error_text("请求路径错误")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ok")

    def do_POST(self):
        if self.path != "/recognize":
            self.send_error_text("请求路径错误")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1_000_000:
                raise ValueError("invalid request size")
            payload = json.loads(self.rfile.read(length))
            image_text = payload["image"]
            if "," in image_text and image_text.startswith("data:"):
                image_text = image_text.split(",", 1)[1]
            image = base64.b64decode(image_text, validate=True)
            result = ocr.classification(image)
            response = json.dumps({"text": result}).encode("utf-8")
        except (binascii.Error, KeyError, OSError, RuntimeError, TypeError, ValueError):
            self.send_error_text("验证码识别失败")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 9103), Handler).serve_forever()  # type: ignore[arg-type]
