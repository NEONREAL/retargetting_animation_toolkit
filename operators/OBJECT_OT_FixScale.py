import bpy
from ..constants import get_operator


class OBJECT_OT_FixScale(bpy.types.Operator):
    bl_idname = get_operator("fix_scale")
    bl_label = "Dummy Operator"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        rig = context.scene.move_props["source_rig"]
        scale_factor = rig.scale[0]
        action = rig.animation_data.action

        for fcurve in action.fcurves:
            if fcurve.data_path.endswith("location"):
                for kp in fcurve.keyframe_points:
                    kp.co[1] *= scale_factor
                fcurve.update()

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        return {"FINISHED"}
