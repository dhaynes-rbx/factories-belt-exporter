import bpy

from .export_belts import AT_OP_ExportBelts
from .add_template_belt import AT_OP_AddTemplateBelt

classes = (
    AT_OP_AddTemplateBelt,
    AT_OP_ExportBelts,
)

def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)