from setuptools import setup, find_packages
from os import path

basedir = path.abspath(path.dirname(__file__))
with open(path.join(basedir, "news_description.md"), encoding="UTF-8") as f:
    ld = f.read()

setup(
    classifiers=[
        # 发展时期
        # 'Development Status :: 3 - Alpha',
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # 开发的目标用户
        "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        # "Intended Audience :: End Users/Desktop",
        # 属于什么类型
        "Topic :: Communications :: File Sharing",
        "Topic :: Internet",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: CD Audio",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        # 许可证信息
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        # 目标 Python 版本
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        # 目前仅支持 Windows 因为其他平台没测试
        "Operating System :: Microsoft :: Windows",
    ],
    name="class163",
    version="0.7.1.6",
    description="网易云音乐部分常用开放信息类API调用和部分需要用户凭证的API调用，包括音乐、歌单、搜索结果的获取，以及音乐的获取及信息写入。",
    long_description=ld,
    long_description_content_type="text/markdown",
    author="CooooldWind_",
    url="https://gitee.com/CooooldWind/class163",
    packages=find_packages(),
    package_data={"": ["*.md"]},
    install_requires=[
        "netease_encode_api",
        "typing_extensions",
    ],
    entry_points={},
)
