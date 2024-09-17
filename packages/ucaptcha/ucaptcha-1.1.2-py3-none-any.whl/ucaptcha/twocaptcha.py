import time
from typing import Any

import httpx

from ucaptcha import logger
from ucaptcha.exceptions import TimeoutError
from ucaptcha.exceptions import UCaptchaError
from ucaptcha.proxies import get_proxy_parts


def solve_twocaptcha(
    api_key: str,
    site_key: str,
    url: str,
    rqdata: str | None = None,
    proxy: str | None = None,
    invisible: bool = True,
) -> str:
    logger.info("Initiating captcha task...")
    parts = get_proxy_parts(proxy)

    typ = "HCaptchaTask" if proxy else "HCaptchaTaskProxyless"

    data: dict[str, Any] = {
        "clientKey": api_key,
        "task": {
            "type": typ,
            "websiteURL": url,
            "websiteKey": site_key,
            "isInvisible": invisible,
        },
    }
    if rqdata is not None:
        data["task"]["enterprisePayload"] = {"rqdata": rqdata}

    if proxy is not None and parts is not None:
        data["task"]["proxyType"] = parts["type"]
        data["task"]["proxyAddress"] = parts["address"]
        data["task"]["proxyPort"] = parts["port"]
        if "username" in parts:
            data["task"]["proxyLogin"] = parts["username"]
        if "password" in parts:
            data["task"]["proxyPassword"] = parts["password"]

    request_url = "https://api.2captcha.com/createTask"
    res = httpx.post(request_url, json=data, timeout=30)
    res.raise_for_status()
    data = res.json()
    if "taskId" not in data:
        raise UCaptchaError("Task ID not found.")
    task_id = data["taskId"]

    time.sleep(7)

    for _ in range(10):
        data = {"clientKey": api_key, "taskId": task_id}
        res = httpx.post(
            "https://api.2captcha.com/getTaskResult", json=data, timeout=30
        )
        res.raise_for_status()
        data = res.json()
        if data["status"] == "processing":
            logger.info("Captcha not ready...")
            time.sleep(10)
            continue
        if data["status"] == "ready":
            logger.info("Captcha ready.")
            return data["solution"]["token"]
        time.sleep(10)
    raise TimeoutError
