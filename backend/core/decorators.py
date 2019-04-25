from flask_jwt_extended import get_current_user

from backend.core.enums import UsersRole
from backend.core.errors import InsufficientRights, WrongApplicationCode
from backend.core.models import Users


def user_some_role_required(roles: [UsersRole]):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            user: Users = get_current_user()
            if user is None:
                print('User not found. Probably @jwt_required decorator missing')

                raise WrongApplicationCode

            for role in roles:
                if user.role == role.value:
                    return fn(*args, **kwargs)

            raise InsufficientRights

        return wrapper

    return decorator


def user_role_required(role: UsersRole):
    return user_some_role_required([role])


def candidate_role_required(fn):
    return user_role_required(UsersRole.CANDIDATE)(fn)


def staff_role_required(fn):
    return user_role_required(UsersRole.STAFF)(fn)


def manager_role_required(fn):
    return user_role_required(UsersRole.MANAGER)(fn)


def university_staff_only(fn):
    return user_some_role_required([UsersRole.MANAGER, UsersRole.STAFF])(fn)
