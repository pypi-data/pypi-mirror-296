import time
from typing import Any

import httpx

from ucaptcha import logger
from ucaptcha.exceptions import TimeoutError
from ucaptcha.exceptions import UCaptchaError
from ucaptcha.proxies import get_proxy_parts


def solve_nopecha(
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
        "key": api_key,
        "type": "hcaptcha",
        "url": url,
        "sitekey": site_key,
        "data": {"rqdata": rqdata},
        "useragent": user_agent,
    }

    if proxy is not None and parts is not None:
        data["proxy"] = {
            "host": parts["address"],
            "port": parts["port"],
            "scheme": parts["type"],
        }

        if "username" in parts:
            data["proxy"]["username"] = parts["username"]
        if "password" in parts:
            data["proxy"]["password"] = parts["password"]

    request_url = "https://api.nopecha.com/token/"
    res = httpx.post(request_url, json=data, timeout=300)
    res.raise_for_status()
    data = res.json()
    if "data" in data:
        task_id = data["data"]
    else:
        raise UCaptchaError(f"{res.status_code}, {res.text}")

    time.sleep(7)

    task_url = f"https://api.nopecha.com/token/?key={api_key}&id={task_id}"

    for _ in range(10):
        res = httpx.get(task_url, timeout=300)
        if res.status_code == 409:
            if "Incomplete job" in res.text:
                logger.info("Captcha not ready...")
                time.sleep(10)
                continue
        res.raise_for_status()
        data = res.json()

        if "data" in data:
            logger.info("Captcha ready.")
            return data["data"]

        raise UCaptchaError(f"{res.status_code}, {res.text}")
    raise TimeoutError
