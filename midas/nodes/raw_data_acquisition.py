"""
Obtain raw data from various sources
"""

import logging
from typing import Any, Dict

from requests import Response

log = logging.getLogger(__name__)


def response_to_json(response: Response) -> Dict[str, Any]:
    data: Dict[str, Any] = response.json()

    return data
