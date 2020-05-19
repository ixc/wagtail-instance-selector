def user_can_access_admin(user):
    if not user:
        return False
    return (
        user.is_superuser or user.is_staff or user.has_perm("wagtailadmin.access_admin")
    )
