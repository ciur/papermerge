from persisting_theory import Registry


class UserMenuRegistry(Registry):
    # the package where the registry will try to find callbacks in each app
    look_into = "user_menu"

user_menu_registry = UserMenuRegistry()  # noqa