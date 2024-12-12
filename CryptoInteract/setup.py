# setup.py
from setuptools import setup, find_packages

setup(
    name='cryptohack',
    packages=find_packages(),
    install_requires=[
        'pwntools',  # 列出依赖的第三方库
    ],
    python_requires='>=3.6',  # 指定支持的 Python 版本
)