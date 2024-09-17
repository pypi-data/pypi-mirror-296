import logging

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    raise ImportError(
        "The 'slack_sdk' package is required to use the Slack backend."
        "You can install it with 'pip install dmf-utils[alerts]'."
    )

from .backend import AlertBackend, AlertException
from ..env import env

__all__ = ["SlackBackend"]

DEFAULT_CHANNEL_ENV = "DMF_DEFAULT_CHANNEL"


class SlackBackend(AlertBackend):
    """
    A backend for sending alerts through Slack.

    This class allows you to send alerts to a specified Slack channel using a bot token.
    It supports sending plain text messages, as well as messages with attachments.

    To use this backend, you'll need to provide a Slack bot token and specify a channel
    where the alerts should be sent.

    **Getting a Slack Token**:
    
    1. Go to the Slack API page and create a new Slack App: https://api.slack.com/apps
    2. Under "OAuth & Permissions", generate a "Bot User OAuth Token".
    3. This token is required to authenticate your bot and should be passed as the `token` parameter.
    4. Ensure the following OAuth scopes are granted to your app:
       - `chat:write`: Allows the bot to send messages to channels.
       - `files:write`: Allows the bot to upload and share files in channels.
       - `chat:write.public`: Allows the bot to post in public channels without being specifically invited to them.

    **Channel Parameter**:
    
    - The `channel` parameter can be either the name (e.g., "#general") or the ID (e.g., "C01234567") 
      of a Slack channel.
    - The channel can be public or private.
    - If you're sending messages to a private channel, ensure that your Slack bot has been invited to that channel.

    **Example Usage**:

    To send a simple message using the Slack backend::

        backend = SlackBackend(token="xoxb-your-slack-bot-token", channel="#general")
        backend("Hello, world!")

    :param token: The Slack bot token used for authentication. This token is necessary to send messages to Slack.
    :param channel: Optional; The Slack channel where messages should be sent. Can be specified by name or ID. 
                    If not provided, the channel will be determined by the `DMF_DEFAULT_CHANNEL` environment variable.
    :param fail_silently: Optional; If True, errors will be logged instead of raising an exception. Default is True.
    """

    def __init__(
        self, token: str, channel: Optional[str] = None, fail_silently: bool = True
    ):
        """
        Initialize the Slack backend with the token and default channel.

        :param token: The Slack bot token used for authentication. This token is necessary to send messages to Slack.
        :param channel: Optional; The Slack channel where messages should be sent. Can be specified by name or ID.
                        If not provided, the channel will be determined by the `DMF_DEFAULT_CHANNEL` environment variable.
        :param fail_silently: Optional; If True, errors will be logged instead of raising an exception. Default is True.
        """

        super().__init__(fail_silently=fail_silently)
        self.client = WebClient(token=token)
        self.channel = channel or env.getenv(DEFAULT_CHANNEL_ENV)

    def send_message(
        self,
        text: str = "",
        attachment: Optional[Union[str, Path]] = None,
        scheduled_time: Optional[Union[int, datetime]] = None,
    ) -> None:
        """
        Send a message to a Slack channel, optionally with a file attachment or scheduled time.
        Raises AlertException if an error occurs, or if both attachment and scheduled_time are provided.
        """
        if attachment and scheduled_time:
            if not self.fail_silently:
                raise AlertException(
                    "Cannot send a message with both an attachment and a scheduled time."
                )
            else:
                logging.warning(
                    "Cannot send a message with both an attachment and a scheduled time. "
                    "Ignoring scheduled time."
                )
                scheduled_time = None

        try:
            if scheduled_time:
                self._send_scheduled_message(text, self.channel, scheduled_time)
            elif attachment:
                self._send_attachment_message(text, self.channel, attachment)
            else:
                self._send_message(text, self.channel)
        except SlackApiError as error:
            if self.fail_silently:
                logging.error(f"Error sending message: {error.response['error']}")
            else:
                raise AlertException(
                    f"Error sending message: {error.response['error']}"
                ) from error

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} channel={self.channel}>"

    def _send_scheduled_message(
        self, text: str, channel: str, post_at: Union[int, "datetime", "timedelta"]
    ) -> dict:
        """Send a scheduled message to Slack."""

        # Convert timedelta to Unix timestamp if needed
        if isinstance(post_at, timedelta):
            post_at = int((datetime.now() + post_at).timestamp())

        # Convert datetime to Unix timestamp if needed
        if isinstance(post_at, datetime):
            post_at = int(post_at.timestamp())

        return self.client.chat_scheduleMessage(
            channel=channel, text=text, post_at=post_at
        )

    def _send_attachment_message(
        self, text: str, channel: str, attachment: Union[str, Path]
    ) -> dict:
        """Send a message with an attachment to Slack."""
        file_path = str(attachment)  # Ensure the path is a string
        return self.client.files_upload_v2(
            channel=channel, file=file_path, initial_comment=text
        )

    def _send_message(self, text: str, channel: str) -> dict:
        """Send a simple message to Slack."""
        return self.client.chat_postMessage(channel=channel, text=text)
