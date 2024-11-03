import pyotp


def verify_2fa_otp(user, otp: str) -> bool:
    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(otp):
        user.mfa_enabled = True
        user.save()
        return True
    return False
