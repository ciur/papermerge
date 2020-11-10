from persisting_theory import Registry


class UserMenuRegistry(Registry):
    # the package where the registry will try to find callbacks in each app
    look_into = "user_menu"


class NavigationRegistry(Registry):
    """
    Leftside navigation menu registry.

    Leftside nagivation menu is where apps (parts of the system)
    appear.
    """

    # the package where the registry will look into
    look_into = "mg_admin"


class SidebarRegistry(Registry):
    look_into = "mg_admin"


user_menu_registry = UserMenuRegistry()  # noqa
navigation = NavigationRegistry()  # noqa
sidebar = SidebarRegistry()  # noqa

