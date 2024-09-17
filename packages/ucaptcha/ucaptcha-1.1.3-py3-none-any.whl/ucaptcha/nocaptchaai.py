import time
from typing import Any

import httpx

from ucaptcha import logger
from ucaptcha.exceptions import KeyDoesNotExistError
from ucaptcha.exceptions import TimeoutError
from ucaptcha.exceptions import UCaptchaError
from ucaptcha.exceptions import ZeroBalanceError
from ucaptcha.proxies import get_proxy_parts


def raise_error(error_code: str):
    if "Invalid apikey" in error_code:
        raise KeyDoesNotExistError
    if error_code.startswith("402"):
        raise ZeroBalanceError
    raise UCaptchaError(f"Unknown error: {error_code}")


def solve_nocaptchaai(
    api_key: str,
    site_key: str,
    url: str,
    user_agent: str | None = None,
    rqdata: str | None = None,
    proxy: str | None = None,
    enterprise: bool = True,
) -> str:
    logger.info("Initiating captcha task...")
    parts = get_proxy_parts(proxy)

    headers = {"Content-Type": "application/json", "apikey": api_key}

    data: dict[str, Any] = {
        "type": "hcaptcha",
        "url": url,
        "sitekey": site_key,
        "useragent": user_agent,
        "enterprise": enterprise,
    }
    if rqdata is not None:
        data["rqdata"] = rqdata

    if proxy is not None and parts is not None:
        data["proxy"] = {
            "ip": parts["address"],
            "port": parts["port"],
            "type": parts["type"],
        }

        if "username" in parts:
            data["proxy"]["username"] = parts["username"]
        if "password" in parts:
            data["proxy"]["password"] = parts["password"]

    request_url = "https://token.nocaptchaai.com/token"
    res = httpx.post(request_url, json=data, headers=headers, timeout=300)
    res.raise_for_status()
    data = res.json()
    if data["status"] != "created":
        raise_error(data["message"])

    task_url = data["url"]
    time.sleep(7)

    for _ in range(10):
        res = httpx.get(task_url, headers=headers, timeout=300)
        res.raise_for_status()
        data = res.json()
        status = data["status"]
        if status == "failed":
            raise_error(data["message"])
        if status == "processing":
            logger.info("Captcha not ready...")
            time.sleep(10)
            continue
        if status == "processed":
            logger.info("Captcha ready.")
            return data["token"]
        time.sleep(10)
    raise TimeoutError
