import time
from urllib.parse import urljoin

import httpx

from ucaptcha import logger
from ucaptcha.auth import TokenAuth
from ucaptcha.exceptions import TimeoutError


def solve_humancaptcha(
    url: str,
    api_key: str,
    site_key: str,
    rqdata: str | None = None,
) -> str:
    logger.info("Initiating captcha task...")

    auth = TokenAuth(api_key)

    data = {
        "captcha": {
            "rqdata": rqdata,
            "sitekey": site_key,
        },
        "remarks": "League Manager",
    }

    request_url = urljoin(url, "/api/captcha-tasks/")
    res = httpx.post(request_url, auth=auth, json=data, timeout=30)
    res.raise_for_status()
    task_id = res.json()["id"]

    result_url = urljoin(url, f"/api/captcha-tasks/{task_id}/solution/")
    for attempt in range(10):
        time.sleep(5)
        try:
            logger.info(
                f"Attempt {attempt + 1}: Fetching solution via human captcha..."
            )
            res = httpx.get(result_url, auth=auth, timeout=30)
            if (
                res.status_code == 400
                and res.json()["detail"] == "No solution found."
            ):
                continue
            res.raise_for_status()
            data = res.json()
            return data["solution"]
        except httpx.HTTPStatusError as e:
            logger.error(e)
            continue

    raise TimeoutError
