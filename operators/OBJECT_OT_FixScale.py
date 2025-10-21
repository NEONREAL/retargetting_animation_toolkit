import bpy
from ..constants import get_operator


class OBJECT_OT_FixScale(bpy.types.Operator):
    bl_idname = get_operator("fix_scale")
    bl_label = "Dummy Operator"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):        

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

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # restoring old selection set and mode
        bpy.ops.object.select_all(action = 'DESELECT')
        for obj in old_selection:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = old_active
        bpy.ops.object.mode_set(mode=old_mode)

        return {"FINISHED"}
