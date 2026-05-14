def cleanup_social_account(backend, uid, user=None, *args, **kwargs) -> dict[str, object]:
    if user:
        user.profile.avatar = kwargs["response"].get("picture", "")
        user.profile.save()
    return {"user": user}


def activate_user(backend, user, *args, **kwargs) -> None:
    if user:
        user.is_active = True
        user.save()
