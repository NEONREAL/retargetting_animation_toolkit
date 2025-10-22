import bpy  # type: ignore
from ..constants import get_operator


# Define the operator to snap FK bones to IK bones
class OBJECT_OT_GenerateDeformArmature(bpy.types.Operator):
    bl_idname = get_operator("generate_def_arm")
    bl_description = "fill with selected object"
    bl_label = "Generate Deform Armature"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        self.original_rig = context.scene.move_props["target_rig"]
        if self.original_rig is None or self.original_rig.type != 'ARMATURE':
            self.report({'ERROR'}, "No valid rig selected")
            return {'CANCELLED'}

        new_rig_name = self.original_rig.name + "_DEFORM"

        # create new armature object
        arm_data = bpy.data.armatures.new(new_rig_name)
        new_rig = bpy.data.objects.new(new_rig_name, arm_data)
        bpy.context.collection.objects.link(new_rig)

        # make it active
        bpy.ops.object.select_all(action='DESELECT')
        new_rig.select_set(True)
        bpy.context.view_layer.objects.active = new_rig

        bpy.ops.object.mode_set(mode='EDIT')

        # create bones
        orig_bones = self.original_rig.data.bones
        for bone in orig_bones:
            if bone.name.startswith("DEF"):
                new_bone = new_rig.data.edit_bones.new(bone.name)
                new_bone.head = bone.head_local
                new_bone.tail = bone.tail_local
                new_bone.matrix = bone.matrix_local.copy()
        bpy.ops.object.mode_set(mode='OBJECT')

        # add copy transforms constraints
        for bone in new_rig.pose.bones:
            target_bone_name = bone.name
            if target_bone_name in self.original_rig.pose.bones:
                constraint = bone.constraints.new('COPY_TRANSFORMS')
                constraint.target = self.original_rig
                constraint.subtarget = target_bone_name



        return {"FINISHED"}
