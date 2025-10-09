import bpy  # type: ignore
from ..constants import AddonProperties
from ..constants import get_operator


class VIEW3D_PT_UI_Sample(bpy.types.Panel):
    bl_label = "A Fancy Panel!"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category

    def draw(self, context):
        props = context.scene.move_props
        layout = self.layout
        box = layout.box()
        box.prop(props, "source_rig", text="Source")
        box.prop(props, "target_rig", text="Target")
        box.operator(get_operator("bake_animation"), text="bake")
