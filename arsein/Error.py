class BaseRubikaError(Exception):
    def __init__(self, message, code=None, value=None):
        super().__init__(message)
        self.code = code
        self.value = value


class AuthError(BaseRubikaError): ...


class TypeMethodError(BaseRubikaError): ...


class TypeAnti(BaseRubikaError): ...


class ErrorServer(BaseRubikaError): ...


class ErrorMethod(BaseRubikaError): ...


class ErrorPrivatyKey(BaseRubikaError): ...


class NOT_REGISTERED(BaseRubikaError): ...


class TOO_REQUESTS(BaseRubikaError): ...


class Connection_Error(BaseRubikaError): ...
