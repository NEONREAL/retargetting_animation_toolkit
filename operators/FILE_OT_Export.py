import bpy  # type: ignore
import os
from ..constants import get_operator


class FILE_OT_Export(bpy.types.Operator):
    bl_idname = get_operator("export")
    bl_label = "Dummy Operator"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        rig = context.scene.move_props["source_rig"]
        action = rig.animation_data.action
        props = context.scene.move_props
        name = props["name"]
        if not name.endswith(".fbx"):
            name += ".fbx"

        export_path = os.path.join(props["directory"], name)

        bpy.ops.export_scene.fbx(
            filepath=export_path,
            use_selection=True,
            apply_scale_options="FBX_SCALE_UNITS",
            object_types={"ARMATURE"},
            add_leaf_bones=False,
            use_armature_deform_only=True,
        )

        return {"FINISHED"}
