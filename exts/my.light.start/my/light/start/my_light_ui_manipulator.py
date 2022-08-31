import omni.ui as ui
import omni.usd

field = ui.StringField()
class Layout(omni.ext.IExt):
    """TreeView示例"""
    def InitLayout(self):

        with ui.ScrollingFrame(
            height=200,
            horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
            vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,
            style_type_name_override="TreeView",
        ):
            self._model = Model("Root", "Items")
            ui.TreeView(self._model, root_visible=False, style={"margin": 0.5})
            # model = MyStringModel()
            # field.model = model
            # ui.StringField(field.model)
class Item(ui.AbstractItem):
    """Single item of the model"""

    def __init__(self, text):
        super().__init__()
        self.name_model = ui.SimpleStringModel(text)
        self.children = None

class Model(ui.AbstractItemModel):
    def __init__(self, *args):
        super().__init__()
        self._children = [Item(t) for t in args]

    # # 编辑时的颜色
    # def begin_edit(self):
    #     custom_treeview.set_style({"color":0xFF00B976})
    # def end_edit(self):
    #     custom_treeview.set_style({"color":0xFFCCCCC})

    def get_item_children(self, item):
        """Returns all the children when the widget asks it."""
        if item is not None:
            if not item.children:
                item.children = [Item(f"Child #{i}") for i in range(5)]
            return item.children

        return self._children

    def get_item_value_model_count(self, item):
        """The number of columns"""
        return 1

    def get_item_value_model(self, item, column_id):
        """
        Return value model.
        It's the object that tracks the specific value.
        In our case we use ui.SimpleStringModel.
        """
        return item.name_model
# class MyStringModel(ui.SimpleStringModel):
# 	def __init__(self):
# 		super().__init__()
# 	# 开始编辑时变色
# 	def begin_edit(self):
# 		field.set_style({"color":0xFF00B976})
# 	def end_edit(self):
# 		field.set_style({"color":0xFFCCCCC})
