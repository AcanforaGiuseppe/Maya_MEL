from maya import cmds


def mirror_pose(left):
    left_nurbs = cmds.ls("*_lf_*", typ="nurbsCurve")
    right_nurbs = cmds.ls("*_rt_*", typ="nurbsCurve")
    left_controls = [cmds.listRelatives(
        nurb, p=True)[0] for nurb in left_nurbs]
    right_controls = [cmds.listRelatives(
        nurb, p=True)[0] for nurb in right_nurbs]
    for i in range(len(left_controls)):
        attributes = cmds.listAttr(left_controls[i], keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            if attr.startswith("translate"):
                direction = -1
            else:
                direction = 1

                if left:
                    new_attr = cmds.getAttr(f"{right_controls[i]}.{attr}")
                    cmds.setAttr(
                        f"{left_controls[i]}.{attr}", new_attr * direction)
                else:
                    new_attr = cmds.getAttr(f"{left_controls[i]}.{attr}")
                    cmds.setAttr(
                        f"{right_controls[i]}.{attr}", new_attr * direction)


def mirror_pose_interface():
    window = "win_symmetrical"
    title = "Symmetrical"
    if (cmds.window(window, exists=True)):
        cmds.delete(window)
    window = cmds.window(title=title, widthHeight=(300, 50))
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Left To Right', command="mirror_pose(True)")
    cmds.button(label='Right To Left', command="mirror_pose(False)")
    cmds.showWindow(window)


mirror_pose_interface()
