import bpy  # type: ignore
from ..constants import AddonProperties
from ..constants import get_operator


class VIEW3D_PT_UI_Retargetting(bpy.types.Panel):
    bl_label = "Retargetting"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category

    def draw(self, context):
        props = context.scene.move_props
        layout = self.layout
        box = layout.box()

        # source rig
        source = box.row(align=True)
        source.prop(props, "source_rig", text="Source")
        pick_source_rig = source.operator(
            get_operator("pick_object"), text="", icon="RESTRICT_SELECT_OFF"
        )
        pick_source_rig.rig = "source_rig"

        # target rig
        target = box.row(align=True)
        target.prop(props, "target_rig", text="Target")
        pick_target_rig = target.operator(
            get_operator("pick_object"), text="", icon="RESTRICT_SELECT_OFF"
        )
        pick_target_rig.rig = "target_rig"

        # setting and comfirming rigs
        source_rig = props["source_rig"]
        source_valid = isinstance(source_rig, bpy.types.Object)

        target_rig = props["target_rig"]
        target_valid = isinstance(target_rig, bpy.types.Object)

        # AnimationName
        box.prop(props, "action_name", text="Action Name")

        # scale button
        scale = box.row()
        scale.enabled = source_valid
        scale.operator(get_operator("fix_scale"), text="Prepare")

        # Space Switching section
        space_switch = box.column()

        # source space switch
        if source_valid:
            source_bone = source_rig.pose.bones.get("Hips")
            if source_bone:
                self.draw_space_switch(space_switch, source_bone, "Copy Transforms", "Source:")

        if target_valid:
            target_bone = target_rig.pose.bones.get("ROOT")
            if target_bone:
                self.draw_space_switch(space_switch, target_bone, "Copy Transforms", "Target:")
        
        # bake button
        bake = box.row()
        bake.scale_y = 1.5
        bake.enabled = target_valid and source_valid
        bake.operator(get_operator("bake_animation"), text="bake")

        # warning if mismatched scale
        if source_valid and target_valid:
            if sum(source_rig.scale) != sum(target_rig.scale):
                warning_row = box.row()
                warning_row.alert = True
                warning_row.label(text="Warning! Mismatching scale", icon="ERROR")

        # transforms box
        box = box.box()
        row = box.row()
        row.enabled = False
        if not source_valid or not target_valid:
            row.label(text="select both rigs", icon="INFO")
            return
        if source_valid:
            source_col = row.column()
            source_col.label(text="Source Scale")
            source_col.label(text=f"x {source_rig.scale[0]:.3f}")
            source_col.label(text=f"y {source_rig.scale[1]:.3f}")
            source_col.label(text=f"z {source_rig.scale[2]:.3f}")

        if target_valid:
            target_col = row.column()
            target_col.label(text="Target Scale")
            target_col.label(text=f"x {target_rig.scale[0]:.3f}")
            target_col.label(text=f"y {target_rig.scale[1]:.3f}")
            target_col.label(text=f"z {target_rig.scale[2]:.3f}")


    def draw_space_switch(self, layout, bone, constraint_name, label_text, icon="ORIENTATION_GLOBAL"):
        row = layout.row()
        
        # try to get the constraint
        con = bone.constraints.get(constraint_name)
        if con:
            # read enabled state and display
            is_world = con.enabled
            display_text = "World" if is_world else "Local"
            row.label(text=label_text)
            row.prop(con, "enabled", text=display_text, icon=icon)
        else:
            # fallback if constraint missing
            row.label(text=f"{label_text} (missing constraint)", icon="ERROR")


