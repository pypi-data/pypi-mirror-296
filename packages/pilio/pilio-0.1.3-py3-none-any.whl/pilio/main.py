import requests
from typing import List
from fastapi import FastAPI, Request
import uvicorn
from pilio.pilio_types import *

PINNACLE_SERVER_URL = "https://trypinnacle.dev/api"


app = FastAPI()


class Pinnacle:
    def __init__(self, api_key: str, webhook_url: str):
        """
        Initialize the Pinnacle object with the API key and webhook URL.
        :param api_key: The API key for authentication.
        :param webhook_url: The URL to receive incoming messages.

        :raises Exception: If the initialization fails.
        """
        self.api_key = api_key
        self.webhook_url = webhook_url
        self.headers = {
            "PINNACLE-API-KEY": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            f"{PINNACLE_SERVER_URL}/init",
            json={"webhook_url": self.webhook_url},
            headers=self.headers,
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to send message: {response.status_code}, {response.text}"
            )

    def send(
        self,
        message: Message,
        phone_number: str,
    ):
        """
        Send a message to the specified phone numbers.
        :param message: The message to send.
        :param phone_numbers: A list of phone numbers to send the message to.
        :raises Exception: If the message sending fails.
        :return: The response from the server.
        """
        message_type = self.get_message_type(message)

        response = requests.post(
            f"{PINNACLE_SERVER_URL}/send",
            json={
                "message": (
                    {"cards": [message.to_dict()]}
                    if message_type == "card"
                    else message.to_dict()
                ),
                "message_type": message_type,
                "phone_number": phone_number,
            },
            headers=self.headers,
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to send message: {response.status_code}, {response.text}"
            )
        else:
            return response.json()

    def check_rcs_status(self, phone_number: str):
        """
        Check the status of an RCS message.
        :param message_id: The ID of the message to check.
        :raises Exception: If the status check fails.
        :return: The RCS status of the phone number.
        """
        response = requests.get(
            f"{PINNACLE_SERVER_URL}/check_rcs",
            headers=self.headers,
            params={"phone_number": phone_number},
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to check RCS status: {response.status_code}, {response.text}"
            )
        else:
            return response.json().get("rcsEnabled", False)

    @staticmethod
    def get_message_type(
        message: Message,
    ) -> Union[
        Literal["basic-rcs"],
        Literal["media"],
        Literal["card"],
        Literal["carousel"],
        Literal["sms"],
    ]:
        """
        Get the type of the message.
        :param message: The message to check.
        :raises ValueError: If the message type is invalid.
        :return: The type of the message as a string.
        """
        if isinstance(message, RCSBasicMessage):
            return "basic-rcs"
        elif isinstance(message, RCSMediaMessage):
            return "media"
        elif isinstance(message, Card):
            return "card"
        elif isinstance(message, Carousel):
            return "carousel"
        elif isinstance(message, SMSMessage):
            return "sms"
        raise ValueError("Invalid message type")

    def on_message(self, callback: OnMessageCallback):
        """
        Set a callback function to be called when a message is received.
        :param callback: The callback function to set. Callback function will receive a PayloadData object.
        """

        @app.post("/pilio/inbound_webhook")
        async def inbound(request: Request):
            payload = await request.body()
            payload_data = PayloadData.model_validate_json(payload)
            callback(payload_data)

        uvicorn.run(app, host="0.0.0.0", port=8000)
