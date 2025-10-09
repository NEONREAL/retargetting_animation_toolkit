import bpy  # type: ignore
from ..constants import get_operator
from ..misc import MoveProps


class OBJECT_OT_BakeAnimation(bpy.types.Operator):
    bl_idname = get_operator("bake_animation")
    bl_label = "Dummy Operator"

    def execute(self, context):
        self.target_rig = context.scene.move_props["target_rig"]
        self.source_rig = context.scene.move_props["source_rig"]
        self.fk_bone_dict = MoveProps.FK_bones
        self.ik_bone_dict = MoveProps.IK_bones
        self.root_bone_dict = MoveProps.root_bones
        self.temp_prefix = "uihawdhawhdaw"
        print("I did absolutely nothing!")

        # mute all constraints
        self.mute_constraints()

        # bake roots
        self.add_constraints(self.root_bone_dict)
        self.bake_action(self.root_bone_dict)

        # bake fk
        self.add_constraints(self.fk_bone_dict)
        self.bake_action(self.fk_bone_dict)

        # bake ik
        self.add_constraints(self.ik_bone_dict, ik=True)
        self.bake_action(self.ik_bone_dict)

        # unmute all constraints
        # self.remove_temp_constraints()
        return {"FINISHED"}

    def add_constraints(self, bone_dict, ik=False) -> None:
        for bone in self.target_rig.pose.bones:
            if bone.name in bone_dict:
                target_bone_name, constraint_type = bone_dict[bone.name]

                constraint = bone.constraints.new(constraint_type)
                constraint.name = (
                    f"{self.temp_prefix} Generated, Copies {target_bone_name}"
                )

                constraint.target = self.target_rig if ik else self.source_rig

                constraint.subtarget = target_bone_name

    def mute_constraints(self) -> None:
        for bone in self.target_rig.pose.bones:
            for con in bone.constraints:
                con.mute = True

    def bake_action(self, bone_dict) -> None:
        # select all the proper bones
        for bone in self.target_rig.pose.bones:
            if bone.name in bone_dict.keys():
                bone.bone.select = True

        # bake action
        bpy.ops.nla.bake(
            frame_start=1,
            frame_end=250,
            only_selected=True,
            visual_keying=True,
            clear_constraints=False,
            use_current_action=True,
            bake_types={"POSE"},
        )

    def remove_temp_constraints(self) -> None:
        for bone in self.target_rig.pose.bones:
            for con in bone.constraints:
                con.mute = False
                if con.name.startswith(
                    self.temp_prefix
                ):  # trying to pick a unique name here
                    bone.constraints.remove(con)
