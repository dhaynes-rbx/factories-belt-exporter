def register_addon():
    # Menus
    from ..menu import register_menus
    register_menus()
    # Operators
    from ..operator import register_operators
    register_operators()

def unregister_addon():
    # Menus
    from ..menu import unregister_menus
    unregister_menus()
    # Operators
    from ..operator import unregister_operators
    unregister_operators()