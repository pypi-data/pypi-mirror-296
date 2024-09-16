
import setuptools


setuptools.setup(
    name="littlelog",
    version="0.1.0",
    author="buggist",
    author_email="316114933@qq.com",
    description="Minimalism python logger. ",
    long_description=open('README.md', "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Buggist/LitttleLog",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)


