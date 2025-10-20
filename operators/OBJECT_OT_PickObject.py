import bpy  # type: ignore
from ..constants import get_operator


# Define the operator to snap FK bones to IK bones
class OBJECT_OT_PickObject(bpy.types.Operator):
    bl_idname = get_operator("pick_object")
    bl_description = "fill with selected object"
    bl_label = "Worl"
    bl_options = {"REGISTER", "UNDO"}

    rig: bpy.props.StringProperty()  # type: ignore

    # optional but handy: this will make sure the operator can only run when there is an active object
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected_obj = bpy.context.active_object

        if selected_obj.type != "ARMATURE":
            self.report({"WARNING"}, "Object is not an Armature!")
            return {"FINISHED"}

        props = context.scene.move_props
        props[self.rig] = selected_obj

        return {"FINISHED"}
