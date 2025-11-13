import bpy  # type: ignore
import os
from ..constants import get_operator


class ANIM_OT_Pin(bpy.types.Operator):
    bl_idname = get_operator("pin")
    bl_label = "Pin Selected Bone"
    bl_options = {"REGISTER", "UNDO"}
    is_pinned: bpy.props.BoolProperty(name="Pin Bone", default=True)  # type: ignore

    def execute(self, context):
        if self.is_pinned:
            self.un_pin(context)
        else:
            self.pin(context)
        return {"FINISHED"}
    

    def pin(self, context):
        rig = context.active_object
        if rig is None or rig.type != 'ARMATURE':
            self.report({'ERROR'}, "No valid target rig selected")
            return
        
        bone = context.active_pose_bone
        if not bone:
            self.report({'ERROR'}, "No valid bone selected")
            return
        
        # add empty for pinning
        pin = bpy.data.objects.new(f"{bone.name}_PIN", None)
        pin.empty_display_type = "SPHERE"
        pin.empty_display_size = 0.1
        pin["is_pin"] = True 
        pin["start_frame"] = context.scene.frame_current
        pin["bone_name"] = bone.name
        pin["armature"] = rig
        bpy.context.collection.objects.link(pin)

        # position empty at bone head
        pin.matrix_world = rig.matrix_world @ bone.matrix

        # adding constraint
        constrain_name = "PIN_CONSTRAINT"
        if constrain_name in bone.constraints:
            bone.constraints.remove(bone.constraints["PIN_CONSTRAINT"])

        bone_constraint = bone.constraints.new('COPY_TRANSFORMS')
        bone_constraint.name = constrain_name
        bone_constraint.target = pin

        # keyframing influence
        current_frame = context.scene.frame_current
        bone_constraint.influence = 0.0
        bone_constraint.keyframe_insert(data_path="influence", frame=current_frame - 1)
        bone_constraint.influence = 1.0
        bone_constraint.keyframe_insert(data_path="influence", frame=current_frame)


        # selects pin
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        pin.select_set(True)
        bpy.context.view_layer.objects.active = pin


    def un_pin(self, context):

        shorthands = {
            "IK-CTRL-LowerLeg.R": "Foot R",
            "IK-CTRL-LowerLeg.L": "Foot L",
            "IK-CTRL-LowerArm.R": "Hand R",
            "IK-CTRL-LowerArm.L": "Hand L",
        }
        pin = context.active_object
        armature = pin.get("armature")
        bone_name = pin.get("bone_name")
        start_frame = pin.get("start_frame")
        props = context.scene.move_props
        mode = props.pin_mode

        if armature is None or bone_name is None:
            self.report({'ERROR'}, "No valid pin selected")
            return

        scene = context.scene
        frame_end = scene.frame_current
        frames = frame_end - start_frame

        if frames > 0:
            # Create a new action for the baked motion
            baked_action = bpy.data.actions.new(name=f"{bone_name}_PinBake")
            if not armature.animation_data:
                armature.animation_data_create()
            armature.animation_data.action = baked_action

            # Select the bone and bake its motion into the new action
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')
            bpy.ops.pose.select_all(action='DESELECT')
            armature.data.bones[bone_name].select = True


            bpy.ops.nla.bake(
                frame_start=start_frame,
                frame_end=frame_end,
                only_selected=True,
                visual_keying=True,
                clear_constraints=True,
                use_current_action=True,
                bake_types={'POSE'}
            )
        else:
            self.clean_constraint_keys(armature, bone_name)

        if mode == "NLA":
            self.clean_constraint_keys(armature, bone_name)

            # Push baked action into a new NLA track (context-safe way)
            bpy.ops.object.mode_set(mode='OBJECT')
            ad = armature.animation_data
            track = ad.nla_tracks.new()
            strip_name = f"{bone_name}_PinLayer"

            if bone_name in shorthands:
                strip_name = shorthands[bone_name] + " Pin"

            track.name = strip_name
            strip = track.strips.new(
                name=strip_name,
                start=start_frame,
                action=baked_action
            )
            strip.blend_type = 'REPLACE'
            strip.extrapolation = "NOTHING"

            # creating fresh new action
            new_action = bpy.data.actions.new(name=f"{armature.name}_Action")
            ad.action = new_action

        # Delete pin object
        bpy.data.objects.remove(pin, do_unlink=True)

        # Reselect bone for convenience
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')
        armature.data.bones[bone_name].select = True


    def clean_constraint_keys(self, armature, bone_name):
        if armature.animation_data and armature.animation_data.action:
            action = armature.animation_data.action
            for fc in list(action.fcurves):
                if f'pose.bones["{bone_name}"].constraints["PIN_CONSTRAINT"]' in fc.data_path:
                    action.fcurves.remove(fc)