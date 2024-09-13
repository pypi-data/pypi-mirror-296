"""
authorizer.py: This module defines a Lambda authorizer that validates API requests
by comparing an API key provided in the request headers with a predefined key stored
in environment variables. It includes constant-time string comparison to prevent timing
attacks and logging for debugging purposes.
"""

import os
import logging
import hmac
from typing import Any

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings using a constant-time algorithm to prevent timing attacks.

    Args:
        val1 (str): The first string to compare.
        val2 (str): The second string to compare.

    Returns:
        bool: True if the strings are equal, False otherwise.
    """
    return hmac.compare_digest(val1, val2)


def handler(event: dict[str, Any], context: Any) -> dict[str, bool]:  # pylint: disable=unused-argument
    """
    Lambda function handler to authorize requests based on a custom API key.

    The function checks if the API key provided in the request headers matches
    the API key stored in environment variables. If the keys match, the request
    is authorized.

    Args:
        event (dict): Event data passed to the Lambda function, containing request 
                      information (e.g., headers).
        context (object): Runtime information provided by Lambda (not used in this function).

    Returns:
        dict: A dictionary with the 'isAuthorized' key set to True or False, indicating 
              if the request is authorized.
    """
    try:
        # Get environment variables
        api_key: str = os.environ.get('API_KEY', "")
        header_name: str = os.environ.get('API_KEY_HEADER_NAME', "x-origin-verify").lower()

        # Get headers in lowercase
        headers: dict[str, str] = {k.lower(): v for k, v in event.get('headers', {}).items()}

        # Retrieve the API key from headers
        provided_api_key: str | None = headers.get(header_name)

        # If no API key provided
        if not provided_api_key:
            logger.warning("Missing API key in header: '%s'", header_name)
            return {'isAuthorized': False}

        # Constant time comparison to prevent timing attacks
        is_authorized: bool = constant_time_compare(provided_api_key, api_key)
        return {'isAuthorized': is_authorized}

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error during authorization: '%s'", str(e))
        # Deny access in case of any failure
        return {'isAuthorized': False}
