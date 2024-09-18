from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import List

import requests
import tenacity
from loguru import logger
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

        delay: int = Field(
            0,
            title="Delay (in seconds)",
            description="The delay (in seconds) in to wait before answering. This is useful in case someone sends multiple messages in a row.",
        )
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
            description="The messages that were received in the past in this conversation, from oldest to newest. \n\nThe columns are: \n- from_user: The username of the sender. \n- to_user: The username of the recipient. \n- message: The message content. \n- message_type: The type of message. \n- date_received: The date and time the message was received, e.g. 2024-09-16T09:15:18Z.",
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
        self.delay = init_inputs.delay
        self.check_after = datetime.now(timezone.utc).replace(tzinfo=None)
        super().__init__(init_inputs, outputs)

    def callback(self):
        super().callback()
        self.check_after = datetime.now(timezone.utc).replace(tzinfo=None)

    def _fetch_new_dms(self):
        dms_url = os.environ.get("PLURALLY_INSTA_DMS_URL")
        assert dms_url, "PLURALLY_INSTA_DMS_URL must be set in the environment"

        api_key = os.environ.get("PLURALLY_API_KEY")
        assert api_key, "PLURALLY_API_KEY must be set in the environment"

        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        after_with_delay = self.check_after.timestamp() - self.delay
        after_with_delay_dt = datetime.fromtimestamp(after_with_delay)
        logger.debug(
            f"checking for new dms after {after_with_delay=} {after_with_delay_dt=}"
        )
        res = requests.get(
            dms_url,
            headers=headers,
            params={
                "limit_history": self.history_limit,
                "after": after_with_delay,
            },
        )
        res.raise_for_status()

        data = res.json()
        return data

    def forward(self, _):
        data = self._fetch_new_dms()
        history = data["history"]

        if not history:
            self.outputs = None
            return

        history, last_message = history[:-1], history[-1]
        self.outputs = {
            "new_message_content": last_message["message"],
            "new_message_date_received": last_message["timestamp"],
            "sender_username": last_message["from_user"]["username"],
            "sender_id": last_message["from_user"]["id"],
            "history": Table(
                data=[
                    {
                        "from_user": dm["from_user"]["username"],
                        "to_user": dm["to_user"]["username"],
                        "message": dm["message"],
                        "message_type": dm["message_type"],
                        "date_received": dm["timestamp"],
                    }
                    for dm in history
                ]
            ),
        }

    def serialize(self):
        return super().serialize() | {
            "history_limit": self.history_limit,
            "delay": self.delay,
        }

    DESC = InitSchema.__doc__


class InstagramSendDm(MetaAuth):
    SCOPES = (
        "instagram_basic",
        "instagram_manage_messages",
        "pages_manage_metadata",
        "pages_showlist",
        "business_management",
    )

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

    @tenacity.retry(
        wait=tenacity.wait_fixed(5),
        stop=tenacity.stop_after_attempt(5),
    )
    def _send_message(self, page_access_token, recipient_id, message):
        r = requests.post(
            "https://graph.facebook.com/v20.0/me/messages",
            params={
                "access_token": page_access_token,
            },
            json={
                "recipient": {"id": recipient_id},
                "message": {"text": message},
            },
        )
        try:
            r.raise_for_status()
        except Exception as e:
            logger.exception(e)
            raise ValueError(f"Failed to send message: {r.text}")

    def forward(self, node_input: "InputSchema"):
        page_access_token = os.environ.get("PLURALLY_INSTA_PAGE_ACCESS_TOKEN")
        assert (
            page_access_token
        ), "PLURALLY_INSTA_PAGE_ACCESS_TOKEN must be set in the environment"

        message_left = str(node_input.message)
        # message limit is 1000, split if longer
        recipient_id = node_input.recipient_id
        while len(message_left) > 1000:
            message = message_left[:1000]
            message_left = message_left[1000:]
            self._send_message(page_access_token, recipient_id, message)
        self._send_message(page_access_token, recipient_id, message_left)

    DESC = InitSchema.__doc__


__all__ = ["InstagramNewDm", "InstagramSendDm"]
