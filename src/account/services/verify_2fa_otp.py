import pyotp


def verify_2fa_otp(user, otp: str) -> bool:
    """Verify the provided OTP code for the user and enable 2FA if valid"""

    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(otp):
        user.mfa_enabled = True
        user.save()
        return True
    return False
