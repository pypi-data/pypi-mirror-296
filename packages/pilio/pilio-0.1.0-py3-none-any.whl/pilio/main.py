import requests
from typing import List, Callable
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

PINNACLE_SERVER_URL = "https://api.trypinnacle.app/api"


app = FastAPI()


class PayloadData(BaseModel):
    messageId: int
    humanId: int
    name: str
    type: str
    fromPhone: str
    message: dict
    sent: str


OnMessageCallback = Callable[[PayloadData], None]


class Pinnacle:
    def __init__(self, api_key: str, webhook_url: str):
        self.api_key = api_key
        self.webhook_url = webhook_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
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

    def send(self, title: str, text: str, phone_numbers: List[str]):
        response = requests.post(
            f"{PINNACLE_SERVER_URL}/send",
            json={"title": title, "text": text, "phone_numbers": phone_numbers},
            headers=self.headers,
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to send message: {response.status_code}, {response.text}"
            )
        else:
            return response.json()

    def onMessage(self, callback: OnMessageCallback):
        @app.post("/pilio/inbound_webhook")
        async def inbound(request: Request):
            payload = await request.body()
            payload_data = PayloadData.model_validate_json(payload)
            callback(payload_data)

        uvicorn.run(app, host="0.0.0.0", port=8000)
