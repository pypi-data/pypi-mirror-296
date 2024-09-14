from setuptools import setup, find_packages

setup(
    name="tkwidgets",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["windnd",],
    author="Benti",
    author_email="t3137904401@outlook.com",
    description="A collection of custom Tkinter widgets",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/benti59/tkwidgets",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",  # 有效的分类器
    ],
    python_requires='>=3.6',
)
