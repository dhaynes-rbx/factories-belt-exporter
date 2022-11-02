import bpy

from .export_panel import AT_PT_ExportPanel

classes = (
    AT_PT_ExportPanel,
)

def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_menus():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)