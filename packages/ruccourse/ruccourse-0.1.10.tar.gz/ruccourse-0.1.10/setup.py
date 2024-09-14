from setuptools import setup, find_packages

setup(
    name="ruccourse",
    version="0.1.10",
    packages=find_packages(),
    description="A tool for RUC students to select courses.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="panjd123",
    author_email="xm.jarden@gmail.com",
    license="MIT",
    url="https://github.com/panjd123/RUC-CourseSelectionTool",
    install_requires=[
        "ruclogin",
        "aiohttp",
        "docopt",
    ],
    package_data={
        "ruccourse": [
            "config.ini",
            "json_datas.pkl",
            "courses.json",
            "ruccourse.log",
            "ring.wav",
        ]
    },
    entry_points={
        "console_scripts": [
            "ruccourse=ruccourse.main:entry_point",
        ]
    },
)
