from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="miya-chat",
    version="0.1.13",  # Updated version number
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "boto3",
        "werkzeug",
    ],
    entry_points={
        "console_scripts": [
            "miya-chat=miya_chat.app:main",
        ],
    },
    author="Manav Kundra",
    author_email="your.email@example.com",
    description="A simple chat application using Flask and AWS Bedrock",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/miya-chat",  # Add your GitHub repository URL here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={
        "miya_chat": ["templates/*", "static/*"],
    },
)