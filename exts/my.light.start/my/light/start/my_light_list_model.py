import omni.ui as ui

class LightListItem(ui.AbstractItem):
    def __init__(self,text:str):
        super().__init__()
        self.sub_model = ui.SimpleStringModel(text)

class LightListModel(ui.AbstractItemModel):
	def __init__(self,*args):
		super().__init__()
		self._children = [LightListItem(t) for t in args]
	def get_item_children(self,item):
		if item is not None:
			return[]

		else:
			return self._children
	def get_item_value_model_count(self,item):
		return 1
	def get_item_value_model(self,item,id):
		return item.sub_model