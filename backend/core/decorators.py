from flask_jwt_extended import get_current_user

from backend.core.enums import UsersRole
from backend.core.errors import InsufficientRights
from backend.core.models import Users


def user_role_required(role: UsersRole):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            user: Users = get_current_user()

            if user.role != role.value:
                return fn(*args, **kwargs)

            raise InsufficientRights

        return wrapper

    return decorator


def user_some_role_required(roles: [UsersRole]):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            user: Users = get_current_user()

            for role in roles:
                if user.role == role.value:
                    return fn(*args, **kwargs)

            raise InsufficientRights

        return wrapper

    return decorator


def candidate_role_required(fn):
    return user_role_required(UsersRole.CANDIDATE, fn)


def staff_role_required(fn):
    return user_role_required(UsersRole.STAFF, fn)


def manager_role_required(fn):
    return user_role_required(UsersRole.MANAGER, fn)
