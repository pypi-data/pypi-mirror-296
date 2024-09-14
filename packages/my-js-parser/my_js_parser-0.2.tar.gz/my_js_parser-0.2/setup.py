from setuptools import setup, find_packages

setup(
    name='my_js_parser',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # 列出你的库的依赖项
        "lxml",
        "quickjs"
    ],
    py_modules=['my_js_parser.parser'],
    # 也可以包含其他的元数据，如作者、描述、许可证等
)