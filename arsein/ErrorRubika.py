from .Error import *


class ErrorRubika:
    def __init__(self, ERROR):
        GetErrors = (
            ERROR["status_det"] if "status_det" in ERROR.keys() else ERROR["status"]
        )

        if GetErrors == "INVALID_AUTH":

            raise AuthError(
                "ًUser authentication is invalid and must be re-entered",
                code="INVALID_AUTH",
                value={"status": "expired auth"},
            )

        elif GetErrors == "NOT_REGISTERED":

            raise NOT_REGISTERED(
                "ًThe user's device is not registered and must be registered",
                code="NOT_REGISTERED",
                value={"status": "The device could not be registered."},
            )

        elif GetErrors == "INVALID_INPUT":

            raise ErrorMethod(
                "ًInput value in the method is incorrect",
                code="INVALID_INPUT",
                value={"status": "Pass the correct values to the desired method."},
            )

        elif GetErrors == "TOO_REQUESTS":

            raise TOO_REQUESTS(
                "ًThe number of requests has been exceeded",
                code="TOO_REQUESTS",
                value={
                    "status": "You have executed the specified method more than the allowed limit."
                },
            )

        elif GetErrors == "SERVER_ERROR":

            raise ErrorMethod(
                "ًInput value in the method is incorrect",
                code="SERVER_ERROR",
                value={"status": "The server in question encountered an error."},
            )
