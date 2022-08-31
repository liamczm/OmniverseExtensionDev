from pxr import Tf,Usd,UsdGeom,UsdLux

import omni.ui as ui
from omni.ui import scene as sc
import omni.usd

class LtStartSceneModel(sc.AbstractManipulatorModel):
    def __init__(self)->None:
        super().__init__()

        self.prim = None
        self.current_path=None
        self.stage_listener = None
        self.position = LtStartSceneModel.PositionItem()
        self.intensity = LtStartSceneModel.IntensityItem()

        # 保存当前UsdContext
        self.usd_context = omni.usd.get_context()
        # self._light = None

        # 追踪选择变动
        self.events = self.usd_context.get_stage_event_stream()
        # 自定义on_stage_event
        self.stage_event_delegate = self.events.create_subscription_to_pop(
            self.on_stage_event,name = "Light Selection Update"
        )
    def on_stage_event(self,event):
        """事件方法,只包含了选择变动"""
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
            # 若选择变动，得到新选中物体的路径
            prim_path = self.usd_context.get_selection().get_selected_prim_paths()

            if not prim_path:
                self.current_path = ""
                # 如果没有路径，返回_item_changed
                self._item_changed(self.position)#_item_changed是自带方法，代表item改变
                return

            # 得到当前stage内选中的prim
            stage = self.usd_context.get_stage()
            prim = stage.GetPrimAtPath(prim_path[0])

            # 如果选中的prim不是Imageable激活stage_listener继续监听选择变动
            if not prim.IsA(UsdGeom.Imageable):
                self.prim = None
                if self.stage_listener:
                    self.stage_listener.Revoke()
                    self.stage_listener = None
                return

            # TODO 是啥?自定义notice_changed
            if not self.stage_listener:
                self.stage_listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged,self.notice_changed,stage)

            self.prim = prim
            self.current_path = prim_path[0]

            # 位置变动，新选中物体有新位置
            self._item_changed(self.position)

    class PositionItem(sc.AbstractManipulatorItem):
        """该model item代表位置"""
        def __init__(self) -> None:
            super().__init__()
            self.value = [0,0,0]
    class IntensityItem(sc.AbstractManipulatorItem):
        """该model item代表灯光强度"""
        def __init__(self) -> None:
            super().__init__()
            self.value = 0.0
    def get_item(self,identifier):
        """根据标识符得到数据项目"""
        if identifier == "name":
            return self.current_path
        elif identifier == "position":
            return self.position
        elif identifier == "intensity":
            return self.intensity

    def get_as_floats(self,item):
        """引用自定义方法得到项目数据为浮点数"""
        if item == self.position:
            # 索取位置
            return self.get_position()
        elif item == self.intensity:
            # 索取强度
            return self.get_intensity()
        # TODO 不懂
        if item:
            # 直接从item得到数值
            return item.value
        return []

    def get_position(self):
        """得到当前选中物体位置的方法,用来作为信息显示的位置"""
        # 得到当前stage
        stage = self.usd_context.get_stage()
        if not stage or self.current_path == "":
            return [0,0,0]

        # 直接从USD得到位置
        prim = stage.GetPrimAtPath(self.current_path)
        position = prim.GetAttribute('xformOp:translate').Get()
        return position

    # 得到强度待定
    def get_intensity(self,time:Usd.TimeCode):
        """得到灯光强度"""
        stage = self.usd_context.get_stage()
        if not stage or self.current_path == "":
            return
        prim = stage.GetPrimAtPath(self.current_path)
        intensity = prim.GetIntensityAttr().Get(time)
        #intensity = self._light.GetIntensityAttr().Get(time)
        return intensity

    # 循环所有通知直到找到选中的
    def notice_changed(self,notice:Usd.Notice,stage:Usd.Stage)->None:
        """Tf.Notice呼起,当选中物体变化"""
        #TODO 为什么只改动位置
        for p in notice.GetChangedInfoOnlyPaths():
            if self.current_path in str(p.GetPrimPath()):
                self._item_changed(self.position)

    def destroy(self):
        self.events = None
        self.stage_event_delegate.unsubscribe()
