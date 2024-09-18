from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    # 以下为必需参数
    name='sm-snake',  # 模块名
    version='0.0.2',  # 当前版本
    description='Common tool kit',  # 简短描述
    
    #packages=find_packages(include=['snake', 'snake.*']),  # 包含snake和snake下的所有子包
    packages=find_packages(), # 自动找到项目中导入的模块
    
    # 以下均为可选参数
    long_description="Common tool kit!",# 长描述
    url='https://github.com/ScottMasson/snake', # 主页链接
    author='Scott Masson', # 作者名
    author_email='masson@tutanota.de', # 作者邮箱
    classifiers=[
        'Intended Audience :: Developers', # 模块适用人群
        'Topic :: Software Development', # 给模块加话题标签

    ],
    keywords=['PDF','png2webp','python'],  # 模块的关键词，使用空格分割
    python_requires='>=3.0',  # 模块支持的Python版本
    entry_points={  # 新建终端命令并链接到模块函数
        'console_scripts': [
            'snake=snake.main:main',
        ],
        },
        project_urls={  # 项目相关的额外链接
        'Bug Reports': 'https://github.com/ScottMasson/snake/issues',
        'Source': 'https://github.com/ScottMasson/snake',
    },
)