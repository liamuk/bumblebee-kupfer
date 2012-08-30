__kupfer_name__ = _("Optirun")
__kupfer_actions__ = ("Optirun", "OptiOpenWith")
__description__ = _("Launch applications with the Nvidia GPU")
__version__ = "0.2"
__author__ = "Kumail Jaffer"

import gio

from kupfer import utils
from kupfer.objects import Action, AppLeaf, FileLeaf

class Optirun (Action):
    def __init__(self):
        Action.__init__(self, _("Launch (using Optirun)"))

    def item_types(self):
        yield AppLeaf
    
    def valid_for_item(self, fileobj):
        return True

    def activate(self, app):
        argv = app.object.get_commandline().split(' ')
        for i, arg in enumerate(argv):
            if arg == "%u" or arg == "%U":
                argv.pop(i)
        argv.insert(0, 'optirun')
        utils.spawn_async(argv)

    def get_description(self):
        return "Launch application with the discrete GPU"

    def get_icon_name(self):
        return "bumblebee"

class OptiOpenWith (Action):
    def __init__(self):
        Action.__init__(self, _("Open With... (using Optirun)"))

    def _activate(self, app_leaf, paths, ctx):
        opti_app_leaf_obj = gio.AppInfo("optirun "+app_leaf.object.get_commandline(),
                                        app_leaf.object.get_name())
        opti_app_leaf = AppLeaf(item=opti_app_leaf_obj)
        opti_app_leaf.launch(paths=paths, ctx=ctx)

    def wants_context(self):
        return True

    def activate(self, leaf, iobj, ctx):
        self._activate(iobj, (leaf.object, ), ctx)
    def activate_multiple(self, objects, iobjects, ctx):
        # for each application, launch all the files
        for iobj_app in iobjects:
            self._activate(iobj_app, [L.object for L in objects], ctx)

    def item_types(self):
        yield FileLeaf
    def requires_object(self):
        return True
    def object_types(self):
        yield AppLeaf
    def get_description(self):
        return _("Open with an application using the discrete GPU")
    def get_icon_name(self):
        return "bumblebee"
