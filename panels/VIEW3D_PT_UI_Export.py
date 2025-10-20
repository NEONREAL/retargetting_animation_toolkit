import bpy  # type: ignore
from ..constants import AddonProperties
from ..constants import get_operator


class VIEW3D_PT_UI_Export(bpy.types.Panel):
    bl_label = "Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        props = context.scene.move_props
        box.prop(props, "name", text="Filename")
        box.prop(props, "directory", text="Export Path")
        row = box.row()
        row.scale_y = 1.5
        row.operator(get_operator("export"), text="Export", icon="EXPORT")
