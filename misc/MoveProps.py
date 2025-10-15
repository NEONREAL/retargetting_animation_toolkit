import bpy  # type: ignore


bones = {
    # Left arm
    "UpperArm.L": ("LeftArm", "COPY_ROTATION"),
    "LowerArm.L": ("LeftForeArm", "COPY_ROTATION"),
    "Hand.L": ("LeftHand", "COPY_ROTATION"),
    # Right arm
    "UpperArm.R": ("RightArm", "COPY_ROTATION"),
    "LowerArm.R": ("RightForeArm", "COPY_ROTATION"),
    "Hand.R": ("RightHand", "COPY_ROTATION"),
    # Left Leg
    "UpperLeg.L": ("LeftUpLeg", "COPY_ROTATION"),
    "LowerLeg.L": ("LeftLeg", "COPY_ROTATION"),
    "Foot.L": ("LeftFoot", "COPY_ROTATION"),
    "Toes.L": ("LeftToeBase", "COPY_ROTATION"),
    # Right Leg
    "UpperLeg.R": ("RightUpLeg", "COPY_ROTATION"),
    "LowerLeg.R": ("RightLeg", "COPY_ROTATION"),
    "Foot.R": ("RightFoot", "COPY_ROTATION"),
    "Toes.R": ("RightToeBase", "COPY_ROTATION"),
}
root_bones = {
    "UpperArm.L-ROOT": ("LeftArm", "COPY_ROTATION"),
    "UpperArm.R-ROOT": ("RightArm", "COPY_ROTATION"),
    "UpperLeg.L-ROOT": ("LeftUpLeg", "COPY_ROTATION"),
    "UpperLeg.R-ROOT": ("RightUpLeg", "COPY_ROTATION"),
    "CTRL-Hip": ("Hips", "COPY_TRANSFORMS"),
    "DEF-Spine_001": ("Hips", "COPY_ROTATION"),
    "DEF-Spine_002": ("Spine1", "COPY_ROTATION"),
    "DEF-Spine_003": ("Spine2", "COPY_ROTATION"),
    "DEF-Spine_004": ("Spine3", "COPY_ROTATION"),
    "DEF_Shoulder.L": ("LeftShoulder", "COPY_ROTATION"),
    "DEF_Shoulder.R": ("RightShoulder", "COPY_ROTATION"),
}

# Generate FK_ prefixed dictionary
FK_bones = {f"FK-{k}": v for k, v in bones.items()}

# Generate IK_ prefixed dictionary
IK_bones = {
    "MCH-LowerLeg.L_pole_vector_helper": ("FK-LowerLeg.L", "COPY_TRANSFORMS"),
    "MCH-LowerLeg.R_pole_vector_helper": ("FK-LowerLeg.R", "COPY_TRANSFORMS"),
    "MCH-LowerArm.L_pole_vector_helper": ("FK-LowerArm.L", "COPY_TRANSFORMS"),
    "MCH-LowerArm.R_pole_vector_helper": ("FK-LowerArm.R", "COPY_TRANSFORMS"),
    "IK-CTRL-LowerArm.L": ("FK-Hand.L", "COPY_TRANSFORMS"),
    "IK-CTRL-LowerArm.R": ("FK-Hand.R", "COPY_TRANSFORMS"),
    "IK-CTRL-LowerLeg.L": ("FK-Foot.L", "COPY_TRANSFORMS"),
    "IK-CTRL-LowerLeg.R": ("FK-Foot.R", "COPY_TRANSFORMS"),
}


class MoveProps(bpy.types.PropertyGroup):
    Modes = [("edit", "Edit", ""), ("pose", "Pose", "")]

    source_rig: bpy.props.PointerProperty(type=bpy.types.Object, name="Rig")

    target_rig: bpy.props.PointerProperty(type=bpy.types.Object, name="Rig")

    delete: bpy.props.BoolProperty(name="Delete old Property")

    # etc.
