from typing import Literal

from ucaptcha.anticaptcha import solve_anticaptcha
from ucaptcha.capmonster import solve_capmonster
from ucaptcha.nocaptchaai import solve_nocaptchaai
from ucaptcha.nopecha import solve_nopecha
from ucaptcha.twocaptcha import solve_twocaptcha

CaptchaService = Literal[
    "anti-captcha", "capmonster", "nocaptchaai", "nopecha", "twocaptcha"
]


def solve_captcha(
    service: CaptchaService,
    api_key: str,
    site_key: str,
    url: str,
    user_agent: str | None = None,
    rqdata: str | None = None,
    proxy: str | None = None,
    enterprise: bool = True,
    invisible: bool = True,
) -> str:
    if service == "anti-captcha":
        return solve_anticaptcha(
            api_key, site_key, url, user_agent, rqdata, proxy
        )
    if service == "capmonster":
        return solve_capmonster(
            api_key, site_key, url, user_agent, rqdata, proxy
        )
    if service == "nocaptchaai":
        return solve_nocaptchaai(
            api_key, site_key, url, user_agent, rqdata, proxy, enterprise
        )
    if service == "nopecha":
        return solve_nopecha(
            api_key,
            site_key,
            url,
            user_agent,
            rqdata,
            proxy,
        )
    if service == "twocaptcha":
        return solve_twocaptcha(
            api_key,
            site_key,
            url,
            rqdata,
            proxy,
            invisible,
        )
    raise NotImplementedError(f"{service} captcha service is not implemented.")
