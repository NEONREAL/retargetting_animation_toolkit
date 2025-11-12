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
        # storing old selection set and mode
        old_active = bpy.context.view_layer.objects.active
        old_selection = bpy.context.selected_objects[:]
        old_mode = bpy.context.mode
        
        # prepping scene for selections
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action = 'DESELECT')

        # selecting correct rig
        source_rig = context.scene.move_props["source_rig"]
        source_rig.select_set(True)
        bpy.context.view_layer.objects.active = source_rig


        # applying scale to location keyframes
        scale_factor = source_rig.scale[0]
        action = source_rig.animation_data.action

        for fcurve in action.fcurves:
            if fcurve.data_path.endswith("location"):
                for kp in fcurve.keyframe_points:
                    kp.co[1] *= scale_factor
                fcurve.update()

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        # restoring old selection set and mode
        bpy.ops.object.select_all(action = 'DESELECT')
        for obj in old_selection:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = old_active
        bpy.ops.object.mode_set(mode=old_mode)

    def space_switch(self, context):
        armature = context.scene.move_props["source_rig"]
        MoveProps = context.scene.move_props
        # add empty for baking
        empty = bpy.data.objects.new(f"{armature.name}_PARENT", None)
        empty.empty_display_type = "ARROWS"
        empty.empty_display_size = 0.5
        MoveProps.helper_empty = empty
        bpy.context.collection.objects.link(empty)

        # add constraints to empty
        constraint = empty.constraints.new("COPY_TRANSFORMS")
        constraint.target = armature
        constraint.subtarget = "Hips"

        # calculate total animation range
        action = armature.animation_data.action
        if action.fcurves:
            first = min(fc.keyframe_points[0].co.x for fc in action.fcurves if fc.keyframe_points)
            last  = max(fc.keyframe_points[-1].co.x for fc in action.fcurves if fc.keyframe_points)

        # select and bake animation to empty
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

        # delete curves for hip bone
        bone_name = "Hips"
        for fcurve in list(action.fcurves):
            if bone_name in fcurve.data_path:
                action.fcurves.remove(fcurve)
        hip_bone = armature.pose.bones.get(bone_name)

        # reset hip bone transform
        if not hip_bone:
            return
        hip_bone.location = (0, 0, 0)
        hip_bone.rotation_euler = (0, 0, 0)

        # parent hip bone to empty
        constraint = hip_bone.constraints.new("COPY_TRANSFORMS")
        constraint.target = empty
        pass