from setuptools import setup, find_packages

# 读取 README.md 文件内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='auto_fix',
    version='1.1.5211',
    description='使用AI模型的自动代码修复库.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Feicell',
    author_email='a@love-me.vip',
    packages=find_packages(),
    install_requires=[
        'openai',
        'loguru',
    ],
)