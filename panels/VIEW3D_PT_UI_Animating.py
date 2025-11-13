import bpy  # type: ignore
from ..constants import AddonProperties
from ..constants import get_operator, get_prism_core_utils_active


class VIEW3D_PT_UI_Animating(bpy.types.Panel):
    bl_label = "Cleanup"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Cleanup Tools")
        props = context.scene.move_props

        # Pin Mode Selection
        row = box.row()
        row.prop(props, "pin_mode", expand=True)

        # Pin Selected Bone Button
        row = box.row()
        row.scale_y = 1.5
        if not context.active_object:
            return

        if context.active_object.get("is_pin"):
            row.operator(get_operator("pin"), text="Unpin Bone", icon="UNPINNED").is_pinned = True
            start_frame = context.active_object.get("start_frame")
            frames = context.scene.frame_current - start_frame
            row = box.column()
            if frames < 0:
                row.alert = True
                row.label(text=f"pinned for {frames} frames", icon="PINNED")
                row.label(text="Cant bake animation! (Click unpin for cleanup)", icon="ERROR")
            else:
                row.label(text=f"pinned for {frames} frames", icon="PINNED")
        
        if not context.active_object.get("is_pin"):
            row.operator(get_operator("pin"), text="Pin Bone", icon="PINNED").is_pinned = False