__all__ = ["PrimPathUIModel"]
from pxr import Tf,Usd,UsdGeom,UsdLux

import omni.ui as ui
import omni.usd

class PathValueItem(ui.AbstractItem):
    """单个Item,决定类型"""
    def __init__(self):
        super().__init__()
        self.path_model = ui.SimpleStringModel()
        self.path_children = []

class PrimPathUIModel(ui.AbstractItemModel):
    """代表名称-数值表的model"""
    def __init__(self):
        super().__init__()
        # 示例参数
        self._children = PathValueItem()

    def get_item_children(self, item):
        """当widget询问时返回所有子项"""
        if item is not None:
            return []
        #     return self._children
        # return item.children

    def get_item_value_model_count(self, item):
        """列数"""
        return 1

    def get_item_value_model(self, item, column_id):
        """
        Return value model.
        It's the object that tracks the specific value.
        In our case we use ui.SimpleStringModel.
        """
        return item.path_model

class TreeViewLayout(omni.ext.IExt):
    """灯光TreeView"""
    def __init__(self):
        super().__init__()

        # self._usd_context = omni.usd.get_context()
        # self._selection = self._usd_context.get_selection()
        # self._events = self._usd_context.get_stage_event_stream()
        # self._stage_event_sub = self._events.create_subscription_to_pop(
        #                 self._on_stage_event, name="customdataview"
        #                 )
        # self._selected_primpath_model = ui.SimpleStringModel("-")
    def InitLayout(self):
        with ui.VStack():
            with ui.ScrollingFrame(
                height=200,
                horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,
                style_type_name_override="LtTreeView",
            ):
                self._model = PrimPathUIModel()
                ui.TreeView(self._model, root_visible=False, style={"margin": 0.5})