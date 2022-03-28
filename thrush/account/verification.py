"""Account verification module."""


def send_verification_code(user, code: str, encrypted_code: str):
    """Send verification code to the user.

    Args:
        user (User): user instance.
        code (str): verification code.
        encrypted_code (str): encrypted verification code.

    Todo:
        The logic should be implemented based on the company's requirements.
        For example: send email, send SMS, send message in a messenger, and so on.
    """
