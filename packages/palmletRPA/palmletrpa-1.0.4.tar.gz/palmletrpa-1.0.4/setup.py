import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '1.0.4'
DESCRIPTION = '这是个rpa工具'
LONG_DESCRIPTION = 'palmlet-rpa是一个python版的rpa工具'

setup(
    name="palmletRPA",
    version=VERSION,
    author="yangsheng",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pywin32==227', 'pyscreeze', 'pytweening'],  # 自动安装依赖
    keywords=['rpa', 'palmletRPA', 'palmlet', 'palm'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={'': ['*.pyd']},
    include_package_data=True,
)
