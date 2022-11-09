from pprint import pprint as pp


class AivBlendShapeManager:
    def __init__(self):
        win_name = self.__class__.__name__
        if cmds.window(win_name, q=True, ex=True):
            cmds.deleteUI(win_name)
        cmds.window(win_name)
        cmds.columnLayout(adj=True)
        
        self.weights_tsl = cmds.textScrollList(
        ams=True, dcc=self.activate_shape, sc=self.connect_weights)
        self.weight_fsg = cmds.floatSliderGrp(
            l="Weight", field=True, 
            minValue=0.0, maxValue=1.0, 
            fieldMinValue=0.0, fieldMaxValue=10.0)
        cmds.button(l="Refresh", c=self.refresh)
        cmds.button(l="Reset", c=self.reset)
        
        cmds.setParent("..")
        cmds.showWindow(win_name)
     
    def refresh(self, *args):
        cmds.textScrollList(self.weights_tsl, e=True, ra=True)
        selection = cmds.ls(sl=True)
        if len(selection) != 1:
            cmds.error("You must select exactly 1 object.")
        
        connected_nodes = cmds.listHistory(selection[0])    
        for node in connected_nodes:
            if (cmds.nodeType(node) == "blendShape"):
                self.blend_shape = node
                break
        else:
            cmds.error("No blend shape found.")
        
        weights = cmds.listAttr(self.blend_shape + ".weight", m=True)
        cmds.textScrollList(self.weights_tsl, e=True, append=weights)
        
    def reset(self, *args):
        weights = cmds.listAttr(self.blend_shape + ".weight", m=True)
        for weight in weights:
            cmds.setAttr(self.blend_shape + "." + weight, 0)

    def activate_shape(self, *args):
        self.reset()
        selected_weights = cmds.textScrollList(self.weights_tsl, q=True, si=True)
        for weight in selected_weights:
            cmds.setAttr(self.blend_shape + "." + weight, 1)
        
    def connect_weights(self, *args):
        selected_weights = cmds.textScrollList(self.weights_tsl, q=True, si=True)
        weights_to_connect = [self.blend_shape + "." + weight for weight in selected_weights]
        cmds.connectControl(self.weight_fsg, weights_to_connect)

bsm = AivBlendShapeManager()
