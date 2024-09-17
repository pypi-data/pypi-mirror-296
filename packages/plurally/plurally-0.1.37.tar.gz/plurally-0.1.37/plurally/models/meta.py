from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import List

import requests
from pydantic import BaseModel, Field

from plurally.models.action.format import FormatTable
from plurally.models.misc import Table
from plurally.models.node import Node


class MetaAuth(Node):
    SCOPES: List[str] = None

    class InitSchema(Node.InitSchema): ...

    class InputSchema(Node.InputSchema): ...

    def __init__(self, init_inputs: InitSchema, outputs=None):
        self._token = None
        self._token_expiry = None
        self._service = None
        super().__init__(init_inputs, outputs)

    def token(self):
        now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
        if self._token is None or self._token_expiry < now:
            self.reset()
            self._token, self._token_expiry = self._get_access_token()
        return self._token

    def _get_access_token(self):
        token_url = os.environ.get("PLURALLY_TOKEN_URL")
        assert token_url, "PLURALLY_TOKEN_URL must be set in the environment"

        api_key = os.environ.get("PLURALLY_API_KEY")
        assert api_key, "PLURALLY_API_KEY must be set in the environment"

        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        res = requests.get(
            token_url, headers=headers, params={"scopes": " ".join(self.SCOPES)}
        )
        res.raise_for_status()

        data = res.json()
        token_expiry = datetime.fromisoformat(data["expires_at"])
        return data["access_token"], token_expiry

    def reset(self):
        self._token = None
        self._token_expiry = None
        self._service = None


class InstagramNewDm(MetaAuth):
    SCOPES = (
        "read_page_mailboxes",
        "pages_messaging",
        "pages_show_list",
        "pages_manage_metadata",
        "business_management",
        "instagram_basic",
        "instagram_manage_messages",
    )
    IS_TRIGGER = True

    class InitSchema(MetaAuth.InitSchema):
        """
        Will trigger the flow for each new incoming Instagram direct message sent to the connected account.

        This block requires you to connect your Instagram account to Plurally.
        """

        history_limit: int = Field(
            20,
            description="The number of past messages to fetch in the conversation history.",
        )

    class OutputSchema(BaseModel):
        new_message_content: str = Field(description="The message that was received.")
        sender_username: str = Field(description="The username of the sender.")
        sender_id: int = Field(description="The ID of the sender.")
        new_message_date_received: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
            description="The date and time the message was received.",
            format="date-time",
        )
        history: Table = Field(
            description="The messages that were received in the past in this conversation, from oldest to newest. \n\nThe columns are: \n- from_user: The username of the sender. \n- to_user: The username of the recipient. \n- message: The message content. \n- message_type: The type of message. \n- date_received: The date and time the message was received format DD-MM-YYYY HH:MM:SS.",
            format="table",
            json_schema_extra={
                "hidden-for-example": True,
            },
        )

    def str_adapter(src_node, tgt_node):
        nodes = [
            FormatTable(
                FormatTable.InitSchema(
                    name="Instagram Conversation History Formatter",
                    prefix="[Start of conversation history.]",
                    suffix="[End of conversation history.]",
                    separator="\n",
                    pos_x=(src_node.pos_x + tgt_node.pos_x) / 2,
                    pos_y=(src_node.pos_y + tgt_node.pos_y) / 2,
                    template="From: {from_user}\nTo: {to_user}\nType: {message_type}\nDate: {date_received}\nMessage: {message}",
                )
            )
        ]
        connections = [(0, "history", 1, "table"), (1, "formatted_text", 2, None)]
        return nodes, connections

    ADAPTERS = {"history": {str: str_adapter}}

    def __init__(self, init_inputs: "InitSchema", outputs=None):
        self.history_limit = init_inputs.history_limit
        super().__init__(init_inputs, outputs)
        self.callback_url = None

    def callback(self):
        super().callback()
        if self.callback_url:
            requests.post(self.callback_url)

    def forward(self, _):
        dms_url = os.environ.get("PLURALLY_INSTA_DMS_URL")
        assert dms_url, "PLURALLY_INSTA_DMS_URL must be set in the environment"

        api_key = os.environ.get("PLURALLY_API_KEY")
        assert api_key, "PLURALLY_API_KEY must be set in the environment"

        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        res = requests.get(dms_url, headers=headers)
        res.raise_for_status()

        data = res.json()

        callback = data["callback"]
        history = data["history"]

        history, last_message = history[:-1], history[-1]
        self.callback_url = callback
        self.outputs = {
            "new_message_content": last_message["message"],
            "new_message_date_received": last_message["timestamp"],
            "sender_username": last_message["from_user"],
            "history": Table(
                [
                    {
                        "from_user": dm["from_user"],
                        "to_user": dm["to_user"],
                        "message": dm["message"],
                        "message_type": dm["message_type"],
                        "date_received": datetime.fromisoformat(
                            dm["timestamp"]
                        ).strftime("%d-%m-%Y %H:%M:%S"),
                    }
                    for dm in history
                ]
            ),
        }

    def serialize(self):
        return super().serialize() | {
            "history_limit": self.history_limit,
        }

    DESC = InitSchema.__doc__


class InstagramSendDm(MetaAuth):
    SCOPES = ("instagram_manage_messages",)

    class InitSchema(MetaAuth.InitSchema):
        """
        Sends a direct message to a user on Instagram.

        This block requires you to connect your Instagram account to Plurally.
        """

    class InputSchema(MetaAuth.InputSchema):
        recipient_id: int = Field(
            description="The username of the recipient.",
        )
        message: str = Field(
            description="The message to send.",
        )

    class OutputSchema(BaseModel): ...

    def forward(self, node_input: "InputSchema"):
        page_access_token = os.environ.get("PLURALLY_INSTA_PAGE_ACCESS_TOKEN")
        assert (
            page_access_token
        ), "PLURALLY_INSTA_PAGE_ACCESS_TOKEN must be set in the environment"

        r = requests.post(
            "https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": page_access_token},
            headers={"Content-Type": "application/json"},
            json={
                "recipient": {"id": node_input.recipient_id},
                "message": {"text": node_input.message},
            },
        )
        r.raise_for_status()

    DESC = InitSchema.__doc__


__all__ = ["InstagramNewDm", "InstagramSendDm"]
