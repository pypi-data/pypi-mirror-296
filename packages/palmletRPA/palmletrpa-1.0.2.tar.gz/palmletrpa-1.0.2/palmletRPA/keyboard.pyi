from .utils.tools import error_handle as error_handle
from typing import Literal

class Keyboard:
    """键盘"""
    @staticmethod
    def get_keyboard_keys() -> list:
        """键盘按键"""
    @staticmethod
    def tap(keys: str | list, *, interval: float = 0.05, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        敲击键盘
        Args:
            keys: 键盘按键
            interval: 输入间隔（秒）【默认0.05秒】
            delay_after: 执行后延迟时间【默认延迟0.5秒】
            error_args: 错误处理，终止、忽略、重试次数和重试间隔【单选】
        """
    @staticmethod
    def hotkey(keys: list, *, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        组合键

        Args:
            keys: 键盘按键
            delay_after: 执行后延迟时间【默认延迟0.5秒】
            error_args: 错误处理，终止、忽略、重试次数和重试间隔【单选】
        """
