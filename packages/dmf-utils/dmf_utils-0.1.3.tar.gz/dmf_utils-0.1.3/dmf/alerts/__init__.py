"""dmf.alerts

This package contains utilities for sending notifications.

"""

from .alerts import send_alert, send_message, get_backend
from .decorator import alert

__all__ = ["alert", "send_alert", "send_message", "get_backend"]