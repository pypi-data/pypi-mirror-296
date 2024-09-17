from typing import Optional, TYPE_CHECKING, Tuple, Union
import warnings

from ..utils.typing import Literal
from ..env import env

if TYPE_CHECKING:
    from .backend import AlertBackend
    from datetime import datetime, timedelta
    from pathlib import Path

ALERT_TOKEN = "DMF_ALERTS_TOKEN"  # Environment variable for the alert token

backend = None  # Global variable to store the backend instance

__all__ = ["alert", "send_alert", "send_message", "get_backend"]


def send_message(
    text: str = "",
    attachment: Optional[Union[str, "Path"]] = None,
    scheduled_time: Optional[Union[int, "datetime", "timedelta"]] = None,
) -> None:
    """
    Sends a message using the appropriate backend, encapsulating the logic of retrieving
    the backend and handling attachments and scheduling.

    :param text: The message text to send. This can be any string that you want to send
                 as the body of the message. If no text is provided, an empty message
                 will be sent.

    :param attachment: Optional; Path to the file to attach. If provided, the file located
                       at this path will be sent as an attachment with the message.
                       The path can be specified as a string or a `Path` object.

    :param scheduled_time: Optional; Time when the message should be sent. This can be
                           specified as a `datetime` object or a `timedelta` object.
                           If a `timedelta` is provided, it will be added to the current time
                           to calculate the scheduled send time.
                           Note that scheduled messages may not be supported by all backends.

    :raises AlertException: If there is an error sending the message.

    **Examples**:

    Sending a simple text message::

        send_message(text="Hello, this is a test message!")

    Sending a message with an attachment::

        send_message(text="Please see the attached document.", attachment="/path/to/document.pdf")

    Scheduling a message to be sent in the future (using timedelta)::

        from datetime import timedelta
        send_message(text="This is a scheduled message.", scheduled_time=timedelta(hours=1))

    """
    backend = get_backend()

    if not backend:
        warnings.warn("No alert backend is available. Message not sent.")
        return

    backend.send_message(
        text=text, attachment=attachment, scheduled_time=scheduled_time
    )


def send_alert(
    text: Optional[str] = None,
    attachment: Optional[Union[str, "Path"]] = None,
    params: Optional[dict] = None,
    level: Literal["success", "info", "warning", "error"] = "info",
) -> None:
    """
    Sends a message formatted as an alert with the specified text and alert level.

    The function sends a notification with a message that is styled according to the
    provided `level` (e.g., "success", "info", "warning", "error"). The message can
    include additional parameters that are appended to the text to provide more context.
    The alert message is sent using the appropriate backend.

    :param text: Optional; The message text to send. If not provided, the level will be used as the default message text.
    :param attachment: Optional; Path to the file to attach. If provided, the file located
                       at this path will be sent as an attachment with the message.
                       The path can be specified as a string or a `Path` object.
    :param params: Optional; Dictionary of key-value pairs to include in the alert message.
                   These parameters will be appended to the message text to provide
                   additional details. For example, `{"Duration": "5 minutes", "Status": "Completed"}`
                   would result in the text "Duration: 5 minutes, Status: Completed" being added
                   to the alert message.
    :param level: Optional; The level of the alert message, which determines the format and
                  emphasis of the message. Supported levels are "success", "info", "warning",
                  and "error". The default is "info".

    **Examples**:

    Sending a simple info alert::

        send_alert(text="The process has completed successfully.")

    Sending a warning alert with parameters added to the text::

        send_alert(text="Process took longer than expected.", params={"Duration": "10 minutes"}, level="warning")

    Sending an error alert with an attachment::

        send_alert(text="An error occurred. See the attached log file.", attachmenlogging.warning("No alert backend is available. Message not sent.")t="/path/to/log.txt", level="error")

    """
    # Get or create the backend instance (always storing it globally)
    backend = get_backend()
    if not backend:
        warnings.warn("No alert backend is available. Message not sent.")
        return
    backend.send_alert(text=text, attachment=attachment, params=params, level=level)


def get_backend(
    alert_token: Optional[str] = None, store: bool = True
) -> Optional["AlertBackend"]:
    """
    Get or create an AlertBackend instance. If the global backend is None or store is False, initialize it with resolved credentials.

    :param alert_token: Optional; Slack token to override the environment variable.
    :param store: If True, store the backend instance in the global variable.
    :return: An initialized AlertBackend instance.
    """
    global backend

    # Initialize the backend if needed
    if not store or backend is None:
        alert_token, credential_type = resolve_credentials(alert_token)

        if credential_type == "slack":
            from .slack_backend import SlackBackend

            current_backend = SlackBackend(token=alert_token)
        elif credential_type == "telegram":
            from .telegram_backend import TelegramBackend

            current_backend = TelegramBackend(token=alert_token)
        else:
            current_backend = None

        # Store the backend if required
        if store:
            backend = current_backend
    else:
        # Use the existing backend if already initialized and store is True
        current_backend = backend

    return current_backend


def resolve_credentials(
    alert_token: Optional[str] = None,
) -> Tuple[Optional[str], Optional[Literal["slack", "telegram"]]]:
    """
    Resolve the credentials for the alert system. Look for environment variables, or use provided overrides.

    :param alert_token: Optional; Slack token to override the environment variable.
    :return: A tuple containing the alert_token and the backend type ('slack').
    """
    alert_token = alert_token or env.getenv(ALERT_TOKEN)

    if not alert_token:
        return None, None

    if alert_token.startswith("xoxb-"):
        credential_type = "slack"
    # Check if the token is a Telegram token format

    elif len(alert_token.split(":")) == 2:
        credential_type = "telegram"
    else:
        credential_type = None

    return alert_token, credential_type
