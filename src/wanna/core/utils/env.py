import os
from typing import Optional

from wanna.core.loggers.wanna_logger import get_logger

logger = get_logger(__name__)


def get_env_bool(value: Optional[str], fallback: bool) -> bool:
    """
    Checks if a str value can be considered True or False,
        mostly used to extract bool values from env vars

    Returns:
        bool from extracted value
    """
    if value in ["False", "false", "0"]:
        return False
    elif value in ["True", "true", "1"]:
        return True
    else:
        return fallback


def _gcp_access_allowed(env_var="WANNA_GCP_ACCESS_ALLOWED"):
    """
    Based on WANNA_GCP_ACCESS_ALLOWED env var checks if wanna can access GCP
    required for on-prem build environments without access to GCP

    Returns:
        bool if wanna can access GCP apis
    """
    allowed = get_env_bool(os.environ.get(env_var), True)
    logger.user_info(f"WANNA GCP access {'NOT ' if not allowed else ''}allowed")
    return allowed


gcp_access_allowed = _gcp_access_allowed()


def _should_validate(env_var="WANNA_GCP_VALIDATION_DISABLED"):
    """
    Based on WANNA_GCP_VALIDATION_DISABLED env var checks if wanna should
    run remote validations that access GCP APIs.

    This is mostly to improve development experience, as it can be slow to allways
    run remote validations

    Returns:
        bool if wanna can access GCP apis
    """
    validate = get_env_bool(os.environ.get(env_var), True)
    if validate:
        logger.user_info("WANNA remote validation is enabled")
    else:
        logger.user_info("WANNA remote validation is disabled")
    return validate


should_validate = gcp_access_allowed and _should_validate()
