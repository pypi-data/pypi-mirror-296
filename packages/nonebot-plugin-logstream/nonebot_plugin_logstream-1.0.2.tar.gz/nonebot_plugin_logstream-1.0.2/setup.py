from distutils.core import setup
from setuptools import find_packages

setup(
      long_description=open('README.md', 'r', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      name='nonebot_plugin_logstream',
      version='1.0.2',  # 版本号
      description='NoneBot 网页终端实时log显示/输出插件',
      author='KiKi-XC',
      author_email='kiki.work@hotmail.com',
      url='https://github.com/KiKi-XC/nonebot_plugin_logstream',
      install_requires=[
            'nonebot2>=2.3.3',
            'fastapi>=0.114.0',
            'ansi2html>=1.9.2',
            'sse_starlette>=2.1.3',
            'uvicorn>=0.17.6',
            'loguru>=0.7.2',
            'starlette>=0.37.2'
      ],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Programming Language :: Python :: 3.10',
      ],
      package_data={
            'nonebot_plugin_logstream': ['View/*.html'],  # 指定要包含的文件
      },
      )
