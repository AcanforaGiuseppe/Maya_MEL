from maya import cmds

database = {}
nurbs = cmds.ls("*_ac_*", "*_fk_*", typ="nurbsCurve")
controls = [cmds.listRelatives(nurb, p=True)[0] for nurb in nurbs]


def reset_animation():
    for control in controls:
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            if attr.startswith("translate") or attr.startswith("rotate"):
                cmds.setAttr(f"{control}.{attr}", 0)
            elif attr.startswith("scale"):
                cmds.setAttr(f"{control}.{attr}", 1)

        attributes = cmds.listAttr(control, ud=True, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            dv = cmds.addAttr(f"{control}.{attr}", q=True, defaultValue=True)
            cmds.setAttr(f"{control}.{attr}", dv)


def save_snapshot():
    database.clear()
    for control in controls:
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            if attr.startswith("translate") or attr.startswith("rotate") or attr.startswith("scale"):
                database[f"{control}.{attr}"] = cmds.getAttr(
                    f"{control}.{attr}")
        attributes = cmds.listAttr(control, ud=True, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            database[f"{control}.{attr}"] = cmds.getAttr(
                f"{control}.{attr}")


def apply_snapshot():
    for control in controls:
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            if attr.startswith("translate") or attr.startswith("rotate") or attr.startswith("scale"):
                cmds.setAttr(f"{control}.{attr}",
                             database[f"{control}.{attr}"])
        attributes = cmds.listAttr(control, ud=True, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            cmds.setAttr(f"{control}.{attr}",
                         database[f"{control}.{attr}"])


def reset_animation_interface():
    window = "win_reset_animation"
    title = "Reset Animation"
    if (cmds.window(window, exists=True)):
        cmds.delete(window)
    window = cmds.window(title=title, widthHeight=(300, 70))
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Reset Animation', command="reset_animation()")
    cmds.button(label='Save Snapshot', command="save_snapshot()")
    cmds.button(label='Apply Snapshot', command="apply_snapshot()")
    cmds.showWindow(window)


reset_animation_interface()
