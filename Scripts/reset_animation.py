from maya import cmds


def reset_animation(controls):
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

nurbs = cmds.ls("*_ac_*", "*_fk_*", typ="nurbsCurve")
controls = [cmds.listRelatives(nurb, p=True)[0] for nurb in nurbs]

reset_animation(controls)