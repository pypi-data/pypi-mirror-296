from .utils import Action as Action
from .utils.tools import error_handle as error_handle
from typing import Literal

class Mouse:
    """鼠标"""
    @classmethod
    def get_cursor_pos(cls):
        """获取当前鼠标位置"""
    @classmethod
    def move(cls, x: int, y: int, *, relative_to: Literal['screen', 'active_window'] = 'screen', is_simulate_move: bool = True, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        鼠标移动

        Args:
            x: x坐标
            y: y坐标
            relative_to: 相对于的参照物【默认整个屏幕】
            is_simulate_move: 是否模拟鼠标移动轨迹【默认模拟】
            delay_after: 执行后延迟时间【默认延迟0.5秒】
            error_args: 错误处理，终止、忽略、重试次数和重试间隔【默认终止 - 单选】
        """
    @classmethod
    def wheel(cls, scroll_num: int, way: Literal['up', 'down'], *, interval: float = 0.05, auxiliary_key: Literal['Alt', 'Ctrl', 'Shift', 'Win'] | None = None, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        鼠标滚轮

        Args:
            scroll_num: 滚动次数
            way: 滚动方式
            interval: 滚动间隔时间【默认0.05秒】
            auxiliary_key: 键盘辅助按键【默认不使用】
            delay_after: 执行后延迟时间【默认延迟0.5秒】
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def click(cls, way: Literal['click', 'dbclick', 'press', 'release'] = 'click', button: Literal['left', 'right', 'middle'] = 'left', *, auxiliary_key: Literal['Alt', 'Ctrl', 'Shift', 'Win'] | None = None, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """点击"""
    @classmethod
    def move_to_click(cls, x: int, y: int, button: Literal['left', 'right', 'middle'] = 'left', way: Literal['click', 'dbclick', 'press', 'release'] = 'click', *, is_simulate_move: bool = True, auxiliary_key: Literal['Alt', 'Ctrl', 'Shift', 'Win'] | None = None, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """移动去点击"""
