from maya import cmds

for i in range(10):
    for j in range(10):
        cube = cmds.polyCube()[0]
        cmds.move(i * 3, 0, j * 3, cube)