from maya import cmds

DUPLICATE_NR_COPIES_TF = "duplicate_nr_copies_tf"


def duplicate_on_line(objA, objB, objC, x_number):
    objA_pos = cmds.xform(objA, q=True, t=True, ws=True)
    objB_pos = cmds.xform(objB, q=True, t=True, ws=True)
    step = 1 / (x_number+1)
    for i in range(x_number+1):
        if i == 0:
            continue
        positionX = objA_pos[0] + (objB_pos[0] - objA_pos[0]) * (step*i)
        positionY = objA_pos[1] + (objB_pos[1] - objA_pos[1]) * (step*i)
        positionZ = objA_pos[2] + (objB_pos[2] - objA_pos[2]) * (step*i)
        dup = cmds.duplicate(objC)
        cmds.move(positionX, positionY, positionZ, dup, absolute=True)

    cmds.delete(objC)


def get_selected_objects(*args):
    selection = cmds.ls(selection=True)
    if len(selection) != 3:
        cmds.error("Select 3 objects")
    nr_copies = cmds.textField(DUPLICATE_NR_COPIES_TF, q=True, text=True)
    duplicate_on_line(*selection, int(nr_copies))


def duplicate_on_line_interface():
    window = "win_duplicate_on_line"
    title = "Duplicate on line"
    if (cmds.window(window, exists=True)):
        cmds.delete(window)
    window = cmds.window(title=title, widthHeight=(300, 25))
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(l="Number of copies: ")
    cmds.textField(DUPLICATE_NR_COPIES_TF)
    cmds.setParent("..")
    cmds.button(label='Duplicate on line',
                command=get_selected_objects)
    cmds.setParent("..")
    cmds.showWindow(window)


duplicate_on_line_interface()
