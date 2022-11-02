import bpy, os, json
from mathutils.geometry import interpolate_bezier

from bpy.props import IntProperty, FloatProperty

class AT_OP_AddTemplateBelt(bpy.types.Operator):

    bl_idname = "at.add_template_belt"
    bl_label = "Import template belt"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        bpy.ops.wm.append("")
        return {'FINISHED'}