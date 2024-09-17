import base64
import os
import requests

from smopay import Base


XENDIT_SECRET_KEY = os.getenv("XENDIT_SECRET_KEY")
XP_SUB_ACCOUNT_MARKETPLACE = os.getenv("XP_SUB_ACCOUNT_MARKETPLACE")


class Card(Base):

  def __init__(self):
    self.secret = XENDIT_SECRET_KEY
    Base.__init__(self)


  def charge(self):
    auth_token = self._Base__authenticate()

    data = {
        "external_id": self.ref_id,
        "token_id": self.token_id,
        "authentication_id": self.authentication_id,
        "amount": self.amount,
    }

    self.headers = {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "for-user-id": XP_SUB_ACCOUNT_MARKETPLACE,
    }

    response = requests.post(
        "https://api.xendit.co/credit_card_charges",
        headers=self.headers,
        data=data,
    )
    return response.json()
