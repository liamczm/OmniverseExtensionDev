from omni.ui import scene as sc
import omni.ui as ui

from .my_light_manipulator import LtStartSceneManipulator
from .my_light_model import LtStartSceneModel

class ViewportLtInfo():
    def __init__(self,viewportWindow,ext_id) -> None:
        self.sceneView = None
        self.viewportWindow = viewportWindow

        with self.viewportWindow.get_frame(ext_id):
            self.sceneView = sc.SceneView()

            # 向SceneView中加载Manipulator
            with self.sceneView.scene:
                LtStartSceneManipulator(model = LtStartSceneModel())

            self.viewportWindow.viewport_api.add_scene_view(self.sceneView)

    def __del__(self):
        self.destroy()

    def destroy(self):
        if self.sceneView:
            self.sceneView.scene.clear()

            if self.viewportWindow:
                self.viewportWindow.viewport_api.remove_scene_view(self.sceneView)

        self.viewportWindow = None
        self.sceneView = None