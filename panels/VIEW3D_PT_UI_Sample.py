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
        box.operator(get_operator("fix_scale"), text="Fix Scale")

        source_rig = props["source_rig"]
        target_rig = props["target_rig"]
        row = box.column()
        row.enabled = False
        if sum(source_rig.scale) == sum(target_rig.scale):
            row.label(text="Scale Matches")
        else:
            row.label(
                text=f"Source Scale is  {source_rig.scale[0]}  {source_rig.scale[1]}  {source_rig.scale[2]}"
            )
            row.label(
                text=f"Target Scale is  {target_rig.scale[0]}  {target_rig.scale[1]}  {target_rig.scale[2]}"
            )
