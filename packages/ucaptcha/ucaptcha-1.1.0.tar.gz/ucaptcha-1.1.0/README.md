# ucaptcha

Universal captcha solving python module

## Installation

You can install the package via pip:

```
pip install ucaptcha
```

## Usage

```py
from ucaptcha import solve_captcha

api_key = "..."
site_key = "..."
url = "..."

print(solve_captcha("anti-captcha", api_key, site_key, url))
print(solve_captcha("capmonster", api_key, site_key, url))
print(solve_captcha("twocaptcha", api_key, site_key, url))
print(solve_captcha("nocaptchaai", api_key, site_key, url))
print(solve_captcha("nopecha", api_key, site_key, url))
print(solve_captcha("twocaptcha", api_key, site_key, url))
```

## Limitations

- Only supports HCaptcha

## License

This project is licensed under the terms of the MIT license.
