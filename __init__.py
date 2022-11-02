bl_info = {
    "name": "Factory Layout Exporter",
    "description": "Exports conveyor belt layouts for Factories.",
    "author": "Dustin Haynes",
    "version": (1,0),
    "blender": (3, 0, 0),
    "location": "View3D",
    "category": "3D View"}


def register():
    from .addon.register import register_addon
    print("Factory Layout Exporter for Assessment Tools")
    register_addon()

def unregister():
    from .addon.register import unregister_addon
    unregister_addon()