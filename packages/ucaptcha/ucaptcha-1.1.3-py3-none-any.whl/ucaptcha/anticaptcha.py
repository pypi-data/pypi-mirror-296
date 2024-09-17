import time
from typing import Any

import httpx

from ucaptcha import logger
from ucaptcha.exceptions import KeyDoesNotExistError
from ucaptcha.exceptions import TimeoutError
from ucaptcha.exceptions import UCaptchaError
from ucaptcha.exceptions import WrongUserKeyError
from ucaptcha.exceptions import ZeroBalanceError
from ucaptcha.proxies import get_proxy_parts


def raise_error(error_code: str):
    if error_code == "ERROR_ZERO_BALANCE":
        raise ZeroBalanceError
    elif error_code == "ERROR_WRONG_USER_KEY":
        raise WrongUserKeyError
    elif error_code == "ERROR_KEY_DOES_NOT_EXIST":
        raise KeyDoesNotExistError
    else:
        raise UCaptchaError(f"Unknown error: {error_code}")


def solve_anticaptcha(
    api_key: str,
    site_key: str,
    url: str,
    user_agent: str | None = None,
    rqdata: str | None = None,
    proxy: str | None = None,
) -> str:
    logger.info("Initiating captcha task...")
    parts = get_proxy_parts(proxy)
    data: dict[str, Any] = {
        "clientKey": api_key,
        "task": {
            "type": "HCaptchaTaskProxyless",
            "websiteURL": url,  # isInvisible removed
            "userAgent": user_agent,
            "websiteKey": site_key,
            "enterprisePayload": {"rqdata": rqdata},
        },
    }
    if proxy is not None and parts is not None:
        data["task"]["type"] = "HCaptchaTask"
        data["task"]["proxyType"] = parts["type"]
        data["task"]["proxyAddress"] = parts["address"]
        data["task"]["proxyPort"] = parts["port"]
        if "username" in parts:
            data["task"]["proxyLogin"] = parts["username"]
        if "password" in parts:
            data["task"]["proxyPassword"] = parts["password"]

    request_url = "https://api.anti-captcha.com/createTask"
    res = httpx.post(request_url, json=data, timeout=300)
    res.raise_for_status()

    data = res.json()
    if data["errorId"] > 0:
        raise_error(data["errorCode"])
    if "taskId" not in data:
        raise UCaptchaError("Task ID not found in data.")
    task_id = data["taskId"]

    for _ in range(10):
        data = {"clientKey": api_key, "taskId": task_id}
        request_url = f"https://api.anti-captcha.com/getTaskResult"
        res = httpx.post(request_url, json=data, timeout=300)
        res.raise_for_status()
        data = res.json()
        if data["errorId"] > 0:
            raise_error(data["errorCode"])
        status = data["status"]
        if status == "processing":
            logger.info("Captcha not ready...")
            time.sleep(10)
            continue
        if status == "ready":
            logger.info("Captcha ready.")
            return data["solution"].get("gRecaptchaResponse")
        time.sleep(10)
        continue
    raise TimeoutError
