from .utils import Action as Action
from .utils.tools import error_handle as error_handle
from PIL.Image import Image as Image
from typing import Literal

class UiDetect:
    @staticmethod
    def get_image_point(image: str | Image, *, region: Literal['full_screen', 'active_window'] = 'full_screen', grayscale: bool = False, confidence: float = 0.999, point: Literal['centre', 'random'] | dict = 'centre', error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        获取图片坐标点
        Args:
            image: 图片路径
            region: 搜索范围
            grayscale: 灰度模式
            confidence: 图片识别精准度
            point: 图片的坐标点
            error_args: 错误处理，终止、忽略、重试次数和重试间隔【单选】
        """
    @staticmethod
    def ocr_code(image):
        """ocr验证码识别"""
