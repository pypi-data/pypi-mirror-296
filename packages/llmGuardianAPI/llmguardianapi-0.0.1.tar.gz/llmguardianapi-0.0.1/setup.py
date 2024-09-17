import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llmGuardianAPI",
    version="0.0.1",
    author="Muhammad Subhan",
    author_email="muhammad.subhan@questlab.pk",
    description="GuardRails API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QuestPK/LLM-Guard.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)