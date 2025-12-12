from setuptools import setup, find_packages

setup(
    name="jobbot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml",
        "python-dotenv",
        "click"
    ],
    entry_points={
        "console_scripts": [
            "jobbot=jobbot.cli:cli",
        ]
    }
)

