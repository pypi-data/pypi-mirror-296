import random
from .utils import tools as tools
from .utils.tools import error_handle as error_handle
from _typeshed import Incomplete
from playwright.sync_api import Browser as Browser, BrowserContext as BrowserContext, Locator as Locator, Page as Page
from typing import Literal, Sequence

class Web:
    """
    浏览器

    error_args:错误处理
    终止：'stop'
    忽略：'ignore'
    重试次数和重试间隔：
    {'retry_num': 0, 'retry_interval': 0}
    """
    browser: Browser
    context: BrowserContext
    page: Page
    @classmethod
    def chromium_page(cls, port: int = 9222):
        """
        启动chrome
        Args:
            port: 端口，默认值为9222端口
        Return:
            RPA能使用的page
        """
    @classmethod
    def connect_page(cls, page: Page = None) -> Page:
        """
        连接page
        Args:
            page: 页面对象
        Returns:
            RPA能使用的page
        """
    @classmethod
    def goto_new_page(cls, context: BrowserContext, locator: Locator, way: Literal['click', 'dbclick'], timeout: float = 20) -> Page:
        """
        跳转新页面
        Args:
            context: 浏览器上下文
            locator: 操作目标
            way: 点击方式，可选：鼠标的点击、双击、中击、右击【默认点击 - 单选】
            timeout: 等待元素存在（s），默认20秒
        Returns:
            返回跳转新页面的page对象
        """
    @classmethod
    def iframe_page(cls, selector_or_index: str | int):
        """
        生成iframe的page
        Args:
            selector_or_index: iframe标签的选择器 或者 iframe标签的索引
        Returns:
            返回iframe框架的page
        """
    @classmethod
    def print_iframe_tree(cls, selector: Incomplete | None = None) -> None:
        """
        打印iframe树
        selector: 需要寻找的元素
        """
    @staticmethod
    def switch_to_page(context, title: Incomplete | None = None, url: Incomplete | None = None):
        """切换指定title名称 或 url 的标签页"""
    @classmethod
    def goto(cls, url: str, wait_until: Literal['commit', 'domcontentloaded', 'load', 'networkidle'] | None = None, timeout: float = 20, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        打开网页
        Args:
            url: 网页地址
            wait_until: 直到加载到什么状态为止
            timeout: 等待元素存在（s），默认20秒
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @staticmethod
    def input(locator: Locator, text: str, *, interval: float = 0.02, is_add_input: bool = False, focus_delay: float = 0.5, timeout: float = 20, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        在网页的输入框中输入内容
        Args:
            locator: 操作目标
            text: 填写要输入的内容
            interval: 输入间隔（s），默认0.02秒
            is_add_input: 是否追加输入
            focus_delay: 获取焦点等待时间（s）， 默认1秒
            delay_after: 执行后延迟（s），默认1秒
            timeout: 等待元素存在（s），默认20秒
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @staticmethod
    def click(locator: Locator, way: Literal['click', 'dbclick'] = 'click', button: Literal['left', 'right', 'middle'] = 'left', *, point: Literal['visible', 'centre', 'random'] | dict = 'visible', auxiliary_key: Sequence[Literal['Alt', 'Control', 'Meta', 'Shift']] | None = None, timeout: float = 20, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        点击网页中的按钮、链接或者其它任何元素
        Args:
            locator: 操作目标
            way: 点击方式，可选：鼠标的点击、双击、中击、右击【默认点击 - 单选】
            button: 鼠标按钮
            point: 目标元素的部位，可选：可见点、随机点、自定义 【默认可见点】
            auxiliary_key: 辅助按键
            timeout: 等待超时时间，默认20秒，单位(s)
            delay_after: 执行后延迟，默认0.5秒，单位(s)
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        Examples:
            web.click(point={locator, point={'ratio_x': 0.5, 'ratio_y': 0.5, 'offset_x': -10, 'offset_y': 0}, auxiliary_key=['Alt', 'Shift'])
        """
    @classmethod
    def hover(cls, locator: Locator, *, timeout: float = 20, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        悬浮
        Args:
            locator: 操作目标
            timeout: 等待超时时间，默认30秒，单位(s)
            delay_after: 执行后延迟，默认1秒，单位(s)
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def set_check(cls, locator: Locator, is_check: bool, *, timeout: float = 20, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        设置复选框，适合type为radio或checkbox

        Args:
            locator: 操作目标
            is_check: 是否勾选复选框
            timeout: 等待超时时间，默认30秒，单位(s)
            delay_after: 执行后延迟，默认1秒，单位(s)
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def wheel(cls, locator: Locator, target: Locator, way: Literal['up', 'down'], *, interval: float = 0.5, duration: float = 30, timeout: float = 20, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        滚轮
        Args:
            locator: 定位的元素
            target: 寻找的目标元素
            way: 滚轮滚动方式，可选 - 向下、向上
            interval: 滚动间隔时间（秒）【默认0.5秒滚动一次】
            duration: 滚动持续超时时间（秒）【默认30秒】
            timeout: 等待超时时间（秒）【默认20秒】
            delay_after: 执行后延迟时间【默认延迟0.5秒】
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def upload_file(cls, locator: Locator, file_path: str, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        上传文件
        Args:
            locator: 操作目标
            file_path: 上传文件路径
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def download_file(cls, locator: Locator, save_path: str, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        下载文件
        Args:
            locator: 操作目标（css、xpath、playwright支持）
            save_path: 下载保存路径
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def drag_and_drop(cls, locator: Locator, target: Locator, *, is_simulate_move: bool = False, timeout: float = 20, delay_after: float = 0.5, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        拖拽
        Args:
            locator: 操作目标
            target: 拖拽的目标
            is_simulate_move: 是否模拟鼠标移动轨迹【默认模拟】
            timeout: 等待超时时间（秒）【默认20秒】
            delay_after: 执行后延迟时间【默认延迟0.5秒】
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @staticmethod
    def get_elem_info(locator: Locator, content: Literal['text', 'attribute'] = 'text', attribute_name: str = None, timeout: float = 20):
        """
        获取元素信息
        Parameters:
            locator: 操作目标
            content: 内容选择 -- 获取元素文本（默认值），获取元素属性
            attribute_name: 属性名称 -- 获取元素属性时，必须填写
            timeout: 等待超时时间（ms），默认30秒
        """
    @staticmethod
    def wait(locator: Locator, state: Literal['visible', 'hidden'] = 'visible', *, timeout: float = 20, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        等待
        Args:
            locator: 操作目标
            state: 状态。visible：等待元素显示, hidden：等待元素隐藏
            timeout: 等待超时时间（s），默认30秒
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
