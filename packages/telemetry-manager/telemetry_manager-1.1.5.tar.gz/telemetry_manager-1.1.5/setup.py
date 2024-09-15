from setuptools import setup, find_packages

setup(
    name="telemetry-manager",
    version="1.1.5",
    author="Nick Smirnov",
    author_email="smbrine@yandex.ru",
    description="A straighthrough manager for python opentelemetry exporter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/smbrine/telemetry-manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
