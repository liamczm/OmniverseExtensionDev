import omni.ext
import omni.ui as ui
import omni.usd
import carb
import omni.kit.commands

from omni.kit.viewport.utility import get_active_viewport_window
# 加载viewport_scene
from .viewport_scene import ViewportLtInfo
from .my_light_model import LtStartSceneModel

from .my_light_ui_model import PrimPathUIModel
from .my_light_ui_manipulator import Layout as layt
from .my_light_ui_model import TreeViewLayout as tVlt
from .my_light_list_model import LightListModel as lst

class MyExtension(omni.ext.IExt):

    def on_startup(self, ext_id):
        # 得到当前usd context
        self._usd_context = omni.usd.get_context()
        self._selection = self._usd_context.get_selection()

        # 注册事件
        self._events = self._usd_context.get_stage_event_stream()
        self._stage_event_sub = self._events.create_subscription_to_pop(
                        self._on_stage_event, name="customdataview"
                        )
        # self._customdata_model = CustomDataAttributesModel()
        self._selected_primpath_model = ui.SimpleStringModel("-")
        self._selected_Prim_Family = ui.SimpleStringModel()
        self._window = ui.Window("ipolog Selection Info", width=300, height=200)
        # 得到当前stage
        self.current_stage = self._usd_context.get_stage()
        #self.list_model = lst(str(self.current_stage))
        # 得到当前激活的视口
        viewport_window = get_active_viewport_window()

        # 如果没有视口记录错误
        if not viewport_window:
            carb.log_error(f"No Viewport to add {ext_id} scene to")
            return

        # 建立scene（覆盖默认的）
        self._viewport_scene = ViewportLtInfo(viewport_window,ext_id)

        self._window = ui.Window("HNADI Light Studio", width=300, height=300)

        #窗口UI
        with self._window.frame:
            with ui.VStack():
                with ui.HStack(height=35):
                    # Pic 占位
                    ui.Circle(
                        name = "iconHolder",
                        radius = 20,
                        size_policy = ui.CircleSizePolicy.FIXED,
                        alignment = ui.Alignment.CENTER,
                    )
                    with ui.VStack():
                        ui.Label("LightType")
                        self._selected_Prim_Family = ui.StringField(model=self._selected_primpath_model,height=20, read_only=True)
                self._selectedPrimName = ui.StringField(model=self._selected_primpath_model, height=20, read_only=True)
                with ui.VStack():
                    ui.Label("Profiles:", height=20)
                    #tVlt.InitLayout(self)
                    #ui.TreeView(self.list_model,root_visible = False)
                with ui.VStack():
                    ui.Label("Lights", height=20)
                    layt.InitLayout(self)
                # 创建按钮
                with ui.HStack():
                    ui.Button("Create a set of lights",clicked_fn=lambda: click_lt())
                    ui.Button("Select",clicked_fn=lambda:select_type())
                def click_lt():
                    omni.kit.commands.execute('CreatePrimWithDefaultXform',
                        prim_type='Xform',
                        attributes={})
                    omni.kit.commands.execute('CreatePrim',
                        prim_type='RectLight',
                        attributes={'width': 100, 'height': 100, 'intensity': 15000})
                    omni.kit.commands.execute('MovePrim',
                        path_from='/World/RectLight_01',
                        path_to='/World/Xform/RectLight_01')
                def select_type(self):
                    selection = self._selection.get_selected_prim_paths()
                    sel_type = selection.select_all_prims(self,type_names="")

                # tree_view = ui.TreeView(
                #     self._customdata_model,
                #     root_visible=False,
                #     header_visible=False,
                #     columns_resizable=True,
                #     column_widths=[ui.Fraction(0.4), ui.Fraction(0.6)],
                #     style={"TreeView.Item": {"margin": 4}},
                # )

    def _on_stage_event(self, event):
        """只跟踪选取变动"""
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
            self._on_selection_changed()


    def _on_selection_changed(self):
        """选择变动后读取信息"""
        selection = self._selection.get_selected_prim_paths()
        stage = self._usd_context.get_stage()
        # print(f"== selection changed with {len(selection)} items")
        if selection and stage:
            #-- set last selected element in property model
            if len(selection) > 0:
                path = selection[-1]
                family = selection
                self._selected_primpath_model.set_value(path)
                self._selected_Prim_Family.set_value(family)

    def on_shutdown(self):
        #清空自定义scene
        if self._viewport_scene:
            self._viewport_scene.destroy()
            self._viewport_scene = None
        print("[my.light.start] MyExtension shutdown")
