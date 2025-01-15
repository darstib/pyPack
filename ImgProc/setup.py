# setup.py
from setuptools import setup, find_packages

setup(
    name="imgProc",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "opencv-python",
        "Pillow",
    ],
    python_requires=">=3.7",  # 指定支持的 Python 版本
)
