class UCaptchaError(Exception):
    pass


class WrongUserKeyError(UCaptchaError):
    pass


class ZeroBalanceError(UCaptchaError):
    pass


class KeyDoesNotExistError(UCaptchaError):
    pass


class ProxyFormatError(UCaptchaError):
    pass


class TimeoutError(UCaptchaError):
    pass
