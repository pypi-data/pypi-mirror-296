from setuptools import find_packages, setup
from collections import defaultdict


def read_requirements():
    requirements = []
    with open("./requirements.txt") as f:
        for req in f:
            req = req.replace("\n", " ").strip()
            if req and not req.startswith("#"):
                requirements.append(req)
    return requirements


def read_extra_requirements():
    extra_requirements = defaultdict(lambda: [])
    collect_key = None
    collect_keys = []
    with open("./extra-requirements.txt") as f:
        for req in f:
            req = req.replace("\n", " ").strip()
            if req.startswith("#"):
                collect_key = req.split(" ")[1]
                collect_keys.append(collect_key)
                continue
            if collect_key and req:
                extra_requirements[collect_key].append(req)
    for key in collect_keys:
        extra_requirements["all"] += extra_requirements[key]
    return extra_requirements


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="cgpcnn",
    version="0.1.2",
    description="A project featuring methods for optimizing neural networks using PyTorch.",
    package_dir={"cgpcnn": "src"},
    packages=["cgpcnn." + pkg for pkg in find_packages("src")],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrLipa/CGP-CNN-Optimizer",
    author="Tomasz Szkaradek",
    author_email="bilbo.weirdo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=read_requirements(),
    extras_require=read_extra_requirements(),
    python_requires=">=3.10.14",
)
