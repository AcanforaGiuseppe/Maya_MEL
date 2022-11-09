from maya import cmds
import random


def duplicate_on_curve():
    selection = cmds.ls(sl=True)  # string[] $selection = `ls -sl`;

    # pathAnimation -fractionMode true -follow true -followAxis x -upAxis y 
    # -worldUpType "vector" -worldUpVector 0 1 0 -inverseUp false 
    # -inverseFront false -bank false;

    if len(selection) != 2:
        cmds.error("You need to select 2 objects")

    curve_name = selection[0]
    obj_name = selection[1]

    motion_path = cmds.pathAnimation(
        obj_name, curve_name,
        fractionMode=True, follow=True,
        followAxis="x", upAxis="y",
        worldUpType="vector", worldUpVector=(0, 1, 0),
        inverseUp=True, inverseFront=False, bank=False)

    bb_x_max = cmds.getAttr(f"{obj_name}.boundingBoxMaxX")
    bb_x_min = cmds.getAttr(f"{obj_name}.boundingBoxMinX")

    obj_len = (bb_x_max - bb_x_min) * 0.6

    curve_len = cmds.arclen(curve_name)

    nr_duplicates = int(curve_len // obj_len)
    step = 1.0 / nr_duplicates

    for i in range(nr_duplicates):
        cmds.setAttr(f"{motion_path}.uValue", step * i)
        cmds.xform(obj_name, q=True, t=True)
        dup = cmds.duplicate(obj_name)
        rot_x = random.randint(-15, 15)
        if i % 2:
            rot_x += 90
            cmds.rotate(rot_x, 0, 0, dup, r=True, os=True, fo=True)

    cmds.delete(obj_name)


duplicate_on_curve()
