import bpy
from ..constants import get_operator


class OBJECT_OT_FixScale(bpy.types.Operator):
    bl_idname = get_operator("fix_scale")
    bl_label = "Dummy Operator"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        self.applyRotationScale(context)
        self.space_switch(context)
        return {"FINISHED"}

    def applyRotationScale(self, context):
        # store old selection + mode
        old_active = bpy.context.view_layer.objects.active
        old_selection = bpy.context.selected_objects[:]
        old_mode = bpy.context.mode

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        # target rig
        source_rig = context.scene.move_props["source_rig"]
        source_rig.select_set(True)
        bpy.context.view_layer.objects.active = source_rig

        # apply scale to keyframes
        scale_factor = source_rig.scale[0]

        anim_data = source_rig.animation_data
        action = anim_data.action
        slot = anim_data.action_slot

        strip = action.layers[0].strips[0]
        channelbag = strip.channelbag(slot, ensure=False)

        if channelbag:
            for fcurve in channelbag.fcurves:
                if fcurve.data_path.endswith("location"):
                    for kp in fcurve.keyframe_points:
                        kp.co[1] *= scale_factor
                    fcurve.update()

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        # restore selection + mode
        bpy.ops.object.select_all(action='DESELECT')
        for obj in old_selection:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = old_active
        bpy.ops.object.mode_set(mode=old_mode)

    def space_switch(self, context):
        armature = context.scene.move_props["source_rig"]
        MoveProps = context.scene.move_props

        # create helper empty
        empty = bpy.data.objects.new(f"{armature.name}_PARENT", None)
        empty.empty_display_type = "ARROWS"
        empty.empty_display_size = 0.5
        MoveProps.helper_empty = empty
        bpy.context.collection.objects.link(empty)

        # constraint empty to hips
        constraint = empty.constraints.new("COPY_TRANSFORMS")
        constraint.target = armature
        constraint.subtarget = "Hips"

        # get action + channelbag once
        anim_data = armature.animation_data
        action = anim_data.action
        slot = anim_data.action_slot

        strip = action.layers[0].strips[0]
        channelbag = strip.channelbag(slot, ensure=False)

        first = None
        last = None

        if channelbag:
            for fc in channelbag.fcurves:
                if not fc.keyframe_points:
                    continue
                fc.update()
                t_first = fc.keyframe_points[0].co.x
                t_last = fc.keyframe_points[-1].co.x
                first = t_first if first is None else min(first, t_first)
                last = t_last if last is None else max(last, t_last)

        # bake empty
        bpy.ops.object.select_all(action='DESELECT')
        empty.select_set(True)
        bpy.context.view_layer.objects.active = empty

        bpy.ops.nla.bake(
            frame_start=int(first),
            frame_end=int(last),
            only_selected=True,
            visual_keying=True,
            clear_constraints=True,
            use_current_action=True,
            bake_types={"OBJECT"},
        )

        # delete Hips curves
        if channelbag:
            for fc in list(channelbag.fcurves):
                if "Hips" in fc.data_path:
                    channelbag.fcurves.remove(fc)

        hip_bone = armature.pose.bones.get("Hips")
        if not hip_bone:
            return

        # reset Hips
        hip_bone.location = (0, 0, 0)
        hip_bone.rotation_euler = (0, 0, 0)

        # constrain hips to empty
        constraint = hip_bone.constraints.new("COPY_TRANSFORMS")
        constraint.target = empty
