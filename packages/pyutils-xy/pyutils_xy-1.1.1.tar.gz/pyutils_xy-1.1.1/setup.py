# @Coding: UTF-8
# @Time: 2024/9/17 21:40
# @Author: xieyang_ls
# @Filename: setup.py

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyutils_xy",  # 用自己的名替换其中的YOUR_USERNAME_
    version="1.1.1",  # 包版本号，便于维护版本
    author="Sierian",  # 作者，可以写自己的姓名
    author_email="2969643689@qq.com",  # 作者联系方式，可写自己的邮箱地址
    description="A small utils package",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)
