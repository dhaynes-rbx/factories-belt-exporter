import bpy

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Assessment Tools"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


class AT_PT_ExportPanel(View3DPanel, bpy.types.Panel):
    bl_idname = "AT_PT_export_panel"
    bl_label = "Export Conveyor Belts"

    def draw(self, context):
        layout = self.layout
        
        # row = layout.row()
        # row.scale_y = 1.0
        # row.operator_context = 'INVOKE_DEFAULT'
        # row.operator("at.add_template_belt")
        # separator = layout.separator()

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "export_folder", text="")

        # col = row.column()
        # fileLocation = col.operator('object.bex_ot_openfolder', text='', icon='FILE_TICK')

        row = layout.row()
        row.scale_y = 2.0
        row.operator("at.export_belts")

        row = layout.row()
        row.scale_y = 2.0
        row.operator("at.select_belt_meshes")

        # print(fileLocation.path)

        # layout.label(text='Gemini Tools')

        # layout.operator("gem.add_lights", text="Add Lights", icon="LIGHT")
        # layout.operator("gem.solidify", text="Solidify", icon="LIGHT")
        
        