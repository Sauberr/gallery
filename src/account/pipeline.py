from typing import Dict


def cleanup_social_account(
    backend, uid, user=None, *args, **kwargs
) -> Dict[str, object]:
    user.avatar = kwargs["response"]["picture"]
    user.save()
    return {"user": user}


def activate_user(backend, user, *args, **kwargs) -> None:
    if user:
        user.is_active = True
        user.save()
