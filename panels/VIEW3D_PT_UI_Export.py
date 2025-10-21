import bpy  # type: ignore
from ..constants import AddonProperties
from ..constants import get_operator, get_prism_core_utils_active


class VIEW3D_PT_UI_Export(bpy.types.Panel):
    bl_label = "Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        props = context.scene.move_props
        status_row = box.row()
        status_row.enabled = False


        if get_prism_core_utils_active():
            status_row.label(text="Prism Core Utils is active", icon="LINKED")
        else:
            status_row.label(text="no prism tools detected", icon="UNLINKED")
            box.prop(props, "directory", text="Path")
        row = box.row()
        row.scale_y = 1.5
        row.operator(get_operator("export"), text="Export", icon="EXPORT")
