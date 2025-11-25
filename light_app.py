import threading
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import BAC0
import os

# =========== 配置参数 ===========
GATEWAY_IP = '192.168.0.166'
FONT_NAME = 'font.ttf'

LIGHT_MAP = {
    'A 回路': [0, 1],
    'B 回路': [2, 3],
    'C 回路': [4, 5],
    'D 回路': [6, 7],
    '总开关': [8, 8]
}

CURRENT_STATES = {}
for k in LIGHT_MAP:
    CURRENT_STATES[k] = 'unknown'
# ===============================

class LightControlRow(BoxLayout):
    """
    自定义组件：代表界面上的一行
    结构： [ 名称 (A回路) ]  [ 状态指示 (● 已开启) ]  [ 开关按钮 ]
    """
    def __init__(self, name, control_callback, font_name, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 80 # 每一行的高度
        self.padding = 10
        self.spacing = 15

        # 1. 名称标签 (左)
        self.name_label = Label(
            text=name, 
            font_name=font_name, 
            font_size=20, 
            size_hint_x=0.3,
            halign='left', valign='middle'
        )
        self.name_label.bind(size=self.name_label.setter('text_size')) # 让文字左对齐

        # 2. 状态标签 (中)
        self.status_label = Label(
            text="connecting...", 
            font_name=font_name,
            font_size=18,
            color=(0.5, 0.5, 0.5, 1), # 初始灰色
            size_hint_x=0.4
        )

        # 3. 控制按钮 (右)
        self.btn = Button(
            text="操作",
            font_name=font_name,
            font_size=18,
            size_hint_x=0.3,
            background_normal='', # 去除默认背景图，允许自定义颜色
            background_color=(0.2, 0.6, 1, 1) # 蓝色
        )
        self.btn.bind(on_press=control_callback)

        self.add_widget(self.name_label)
        self.add_widget(self.status_label)
        self.add_widget(self.btn)

class LightControlPanel(GridLayout):
    def __init__(self, **kwargs):
        super(LightControlPanel, self).__init__(**kwargs)
        self.cols = 1
        self.padding = 10
        self.spacing = 5
        self.rows_ui = {} # 存每一行的UI对象

        # 检查字体
        self.use_font = FONT_NAME if os.path.exists(FONT_NAME) else 'Roboto'

        # 标题栏
        title = Label(text="广州景雅智能照明控制系统", font_name=self.use_font, font_size=26, size_hint_y=None, height=60, color=(1,1,1,1))
        self.add_widget(title)

        # 系统状态栏
        self.sys_status = Label(text="正在连接网关...", font_name=self.use_font, size_hint_y=None, height=30, color=(1,1,0,1))
        self.add_widget(self.sys_status)

        # 生成每一行
        for name, points in LIGHT_MAP.items():
            # 创建一行
            row = LightControlRow(
                name=name, 
                font_name=self.use_font,
                control_callback=lambda x, n=name, c=points[0]: self.on_button_click(n, c)
            )
            self.add_widget(row)
            self.rows_ui[name] = row

        # BACnet 初始化
        try:
            self.bacnet = BAC0.lite()
            # 启动轮询线程
            t = threading.Thread(target=self.background_polling_loop, daemon=True)
            t.start()
        except:
            self.sys_status.text = "初始化失败！请检查端口占用"
            self.sys_status.color = (1, 0, 0, 1)
            self.bacnet = None

        # 启动界面刷新 (0.5秒一次)
        Clock.schedule_interval(self.update_ui, 0.5)

    def background_polling_loop(self):
        while True:
            try:
                success_count = 0
                for name, points in LIGHT_MAP.items():
                    feed_pt = points[1]
                    val = self.bacnet.read(f'{GATEWAY_IP} binaryValue {feed_pt} presentValue')
                    
                    if str(val).lower() == 'active':
                        CURRENT_STATES[name] = 'active'
                    else:
                        CURRENT_STATES[name] = 'inactive'
                    success_count += 1
                
                if success_count > 0:
                    self.sys_status.text = "系统正常 - 实时监控中"
                    self.sys_status.color = (0, 1, 0, 1)

            except Exception as e:
                self.sys_status.text = "通讯中断"
                self.sys_status.color = (1, 0, 0, 1)
            
            time.sleep(1.0)

    def update_ui(self, dt):
        for name, state in CURRENT_STATES.items():
            row = self.rows_ui[name]
            
            if state == 'active':
                row.status_label.text = "● 已开启"
                row.status_label.color = (0, 1, 0, 1) # 绿色文字
                row.btn.text = "关闭"
                row.btn.background_color = (1, 0.3, 0.3, 1) # 红色按钮(提示去关)
            elif state == 'inactive':
                row.status_label.text = "○ 已关闭"
                row.status_label.color = (0.7, 0.7, 0.7, 1) # 灰色文字
                row.btn.text = "开启"
                row.btn.background_color = (0.2, 0.6, 1, 1) # 蓝色按钮(提示去开)
            else:
                row.status_label.text = "..."

    def on_button_click(self, name, ctrl_pt):
        if not self.bacnet: return
        
        current = CURRENT_STATES[name]
        target = 'inactive' if current == 'active' else 'active'
        
        # 乐观更新UI (让按钮变灰，提示正在处理)
        self.rows_ui[name].btn.text = "..."
        self.rows_ui[name].btn.background_color = (0.5, 0.5, 0.5, 1)

        threading.Thread(target=self._send_cmd, args=(ctrl_pt, target)).start()

    def _send_cmd(self, ctrl_pt, val):
        try:
            self.bacnet.write(f'{GATEWAY_IP} binaryValue {ctrl_pt} presentValue {val}')
        except:
            pass

class LightApp(App):
    def build(self):
        Window.clearcolor = (0.15, 0.15, 0.17, 1) # 高级深灰背景
        return LightControlPanel()

if __name__ == '__main__':
    LightApp().run()
