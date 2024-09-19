from palmletRPA import Book as Book, Range as Range, Sheet as Sheet
from typing import Literal

class Excel:
    workbook: Book
    @classmethod
    def start_workbook(cls, path: str = None, update_links: bool = None, password: str = None, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        启动工作簿
        Args:
            path: 文件路径
            update_links: 更新连接
            password: 密码
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def save_workbook(cls, workbook: Book, save_to: str = None, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        保存工作簿
        Args:
            workbook: 工作簿对象
            save_to: 保存路径
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def close_workbook(cls, workbook: Book, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        关闭工作簿
        Args:
            workbook: 工作簿对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def add_sheet(cls, workbook: Book, *, name: str = None, position: Literal['first', 'last'] = 'first', error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        添加sheet页
        Args:
            workbook: 工作簿对象
            name: 增加的sheet名称
            position: 增加sheet的位置 - first【第一个位置】、last【最后一个位置】
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def active_sheet(cls, sheet: Sheet, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        激活sheet页
        Args:
            sheet: sheet对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def copy_sheet(cls, sheet: Sheet, new_sheet_name: str, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        复制sheet页
        Args:
            sheet: sheet对象
            new_sheet_name: 复制的新sheet名称
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def delete_sheet(cls, sheet: Sheet, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        删除sheet页
        Args:
            sheet: sheet对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def rename_sheet(cls, sheet: Sheet, new_sheet_name: str, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        重命名sheet页
        Args:
            sheet: sheet对象
            new_sheet_name: 新sheet名称
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def get_sheet_name(cls, workbook: Book, sheet_range: Literal['current', 'all'] = 'current', *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        获取sheet页
        Args:
            workbook: 工作簿对象
            sheet_range: sheet范围 - current【当前sheet范围】、all【所有sheet范围】
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def get_rows_count(cls, sheet: Sheet, *, error_args: Literal['stop', 'ignore'] | dict = 'stop') -> int:
        """
        获取总行数
        Args:
            sheet: sheet对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def get_columns_count(cls, sheet: Sheet, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        获取总列数
        Args:
            sheet: sheet对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def write_cell(cls, cell: Range, value: int | str | list, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        写入单元格
        Args:
            cell: 单元格对象
            value: 输入值，支持数值、字符串、一到二维列表、公式
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def read_cell(cls, cell: Range, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        读取单元格
        Args:
            cell: 单元格对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def clear_cell(cls, cell: Range, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        清空单元格内容
        Args:
            cell: 单元格对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def delete_cell(cls, cell: Range, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        删除单元格
        Args:
            cell: 单元格对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def insert_cell(cls, cell: Range, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        插入单元格
        Args:
            cell: 单元格对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def merge_cell(cls, cell: Range, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        合并单元格
        Args:
            cell: 单元格对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
    @classmethod
    def unmerge_cell(cls, cell: Range, *, error_args: Literal['stop', 'ignore'] | dict = 'stop'):
        """
        取消合并单元格
        Args:
            cell: 单元格对象
            error_args: 错误处理，可选，终止、忽略、重试次数和重试间隔【单选】
        """
