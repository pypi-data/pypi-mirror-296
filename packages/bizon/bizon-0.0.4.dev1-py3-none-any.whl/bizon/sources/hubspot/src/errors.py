from typing import Any

from pydantic import Field
from requests import HTTPError

from bizon.common.errors.errors import ErrorTraceMessage, FailureType


class HubspotError(ErrorTraceMessage):
    failure_type: FailureType = Field(FailureType.SYSTEM_ERROR, description="The type of error")


class HubspotTimeout(HTTPError):
    """502/504 HubSpot has processing limits in place to prevent a single client from causing degraded performance,
    and these responses indicate that those limits have been hit. You'll normally only see these timeout responses
    when making a large number of requests over a sustained period. If you get one of these responses,
    you should pause your requests for a few seconds, then retry.
    """


class HubspotInvalidAuth(HubspotError):
    """401 Unauthorized"""


class HubspotAccessDenied(HubspotError):
    """403 Forbidden"""


class HubspotRateLimited(HTTPError):
    """429 Rate Limit Reached"""


class HubspotBadRequest(HubspotError):
    """400 Bad Request"""


class InvalidStartDateConfigError(Exception):
    """Raises when the User inputs wrong or invalid `start_date` in inout configuration"""

    def __init__(self, actual_value: Any, message: str):
        super().__init__(
            f"The value for `start_date` entered `{actual_value}` is ivalid and could not be processed.\nPlease use the real date/time value.\nFull message: {message}"
        )
