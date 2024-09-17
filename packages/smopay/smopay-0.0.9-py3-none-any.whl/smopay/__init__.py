import base64
import os


XENDIT_SECRET_KEY = os.getenv("XENDIT_SECRET_KEY")


class Base:

  def __authenticate(self):
    auth_base64 = base64.b64encode(f"{XENDIT_SECRET_KEY}:".encode())
    return auth_base64.decode("utf-8")
