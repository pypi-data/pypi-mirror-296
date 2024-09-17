# generator.py
# if submenu already exists for the parent menu index
class SubMenuAlreadyExists(Exception):
    pass
# add_submenu function, if parent_identifier doesnot match any
class ParentMenuNotFound(Exception):
    pass
# add_submenu function, if parent_menu_index does not exist.
class ParentIndexNotFound(Exception):
    pass
# handler function, if no menu is defined.
class NoMenuFound(Exception):
    pass
# handler function, if specified menu identifier to start from is not found
class StartIdentifierNotFound(Exception):
    pass
# handler function, if no function is set.
class EndReachedNoFunctionFound(Exception):
    pass