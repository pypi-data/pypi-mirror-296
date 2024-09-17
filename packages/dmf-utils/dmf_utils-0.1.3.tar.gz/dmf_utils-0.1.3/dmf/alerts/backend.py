from typing import Union, Optional, TYPE_CHECKING

from ..utils.typing import Literal

if TYPE_CHECKING:
    from pathlib import Path
    from datetime import datetime, timedelta

__all__ = ["AlertException", "AlertBackend"]

LEVEL_MAPPING = {
    "success": ":white_check_mark:",
    "info": ":books:",
    "warning": ":warning:",
    "error": ":red_circle:",
}

class AlertException(Exception):
    """Exception raised for errors in the alert backend."""

    pass


class AlertBackend:
    """Base class for alert backends."""

    def __init__(self, fail_silently: bool = True) -> None:
        self.fail_silently = fail_silently

    def __call__(
        self,
        text: str = "",
        attachment: Optional[Union[str, "Path"]] = None,
        scheduled_time: Optional[Union[int, "datetime", "timedelta"]] = None,
    ) -> None:
        """Allows the instance to be called like a function to send an alert."""
        try:
            self.send_message(
                text=text, attachment=attachment, scheduled_time=scheduled_time
            )
        except AlertException as error:
            if not self.fail_silently:
                raise error

    def send_message(
        self,
        text: str = "",
        attachment: Optional[Union[str, "Path"]] = None,
        scheduled_time: Optional[Union[int, "datetime"]] = None,
    ) -> None:
        """Placeholder method to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def get_alert_text(
        self,
        text: Optional[str] = None,
        level: Literal["success", "info", "warning", "error"] = "info",
        params: Optional[dict] = None,
        separator: str = "\n      • ",
    ) -> str:
        """Format the notification text with the given arguments."""

        level_emoji = LEVEL_MAPPING.get(level, "")
        text = text or f"{level.capitalize()}:"
        message = f"{level_emoji} {text}"
        if params:
            params_str = separator.join(
                f"*{key}*: {value}" for key, value in params.items()
            )
            message += f"{separator}{params_str}"
        return message

    def send_alert(
        self,
        text: Optional[str] = None,
        attachment: Optional[Union[str, "Path"]] = None,
        params: Optional[dict] = None,
        level: Literal["success", "info", "warning", "error"] = "info",
    ) -> None:
        """Send a notification with a template message."""
        message = self.get_alert_text(text=text, level=level, params=params)
        self.send_message(text=message, attachment=attachment)
