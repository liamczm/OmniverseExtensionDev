from omni.ui import scene as sc
import omni.ui as ui
from warp.types import transform
from omni.ui import color as cl

class LtStartSceneManipulator(sc.Manipulator):
    # 包含model作为参数
    def on_build(self):
        """model变动即呼起,重建整个manipulator"""
        # 没有model返回
        if not self.model:
            return
        # 没有选择返回
        if self.model.get_item("name") == "":
            return

        # 更新位置信息(通过model)
        position = self.model.get_as_floats(self.model.get_item("position"))

        with sc.Transform(transform = sc.Matrix44.get_translation_matrix(*position)):
            # 屏幕上显示名称信息
            with sc.Transform(scale_to = sc.Space.SCREEN):
                sc.Label(f"Path:{self.model.get_item('name')}",color=cl("#76b900"),size = 20)
                #sc.Label(f"Path:{self.model.get_item('intensity')}")
            #sc.Label(f"Path:{self.model.get_item('name')}")

    def on_model_updated(self,item):
        """model中某项目更新呼起该方法,核心,重建Manipulator"""
        # manipulator自带的方法，删除旧的重新执行on_build生成新的manipulator
        self.invalidate()
