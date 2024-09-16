[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<br />
<div align="center">
  <a href="https://github.com/MrLipa/CGP-CNN-Optimizer">
    <img src="references/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Cartesian Genetic Programming for CNN Optimization</h3>

  <p align="center">
     Project for optimizing convolutional neural networks using Cartesian genetic programming! 
    <br />
    <a href="https://github.com/MrLipa/CGP-CNN-Optimizer"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/MrLipa/CGP-CNN-Optimizer">View Demo</a>
    ·
    <a href="https://github.com/MrLipa/CGP-CNN-Optimizer/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/MrLipa/CGP-CNN-Optimizer/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#makefile-commands">Makefile Commands</a></li>
        <li><a href="#makefile-commands-for-windows-using-mingw32-make">Makefile Commands for Windows (using `mingw32-make`)</a></li>
        <li><a href="#slurm-commands">SLURM Commands</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



## About The Project

This project is a framework designed to streamline the optimization of convolutional neural networks (CNNs) using Cartesian Genetic Programming (CGP). It provides a structured environment that follows best practices for machine learning projects, including modularity, scalability, and easy deployment.

The project leverages a **cookiecutter template**, which ensures consistent structure and workflow for your projects.

You can easily fork the repository, suggest changes, or contribute to ongoing improvements!

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

This project is built using several major frameworks and libraries that streamline the development of machine learning models and help with experiment tracking and documentation. Below are the key technologies used:

* ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
* ![PyTorch](https://img.shields.io/badge/PyTorch-1.10%2B-red)
* ![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
* ![MLflow](https://img.shields.io/badge/MLflow-1.20%2B-brightgreen)
* ![Sphinx](https://img.shields.io/badge/Sphinx-4.0%2B-lightgrey)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

To get a local copy of this project up and running, follow these simple steps.

### Prerequisites

You need **Python 3.10** or newer. Below are two options for setting up the environment:

1. **Using Conda:**
   ```sh
   conda create -n cgp-cnn-env python=3.10 -y
   conda activate cgp-cnn-env
   pip install .
   ```

2. **Using venv:**
   ```sh
   python -m venv cgp-cnn-env
   source cgp-cnn-env/bin/activate  # On Windows: cgp-cnn-env\Scripts\activate
   pip install .
   ```

For additional dependencies, install with:
```sh
pip install .[basic]  # or [dev], [doc], [all]
```

Alternatively, install the library directly via pip:
```sh
pip install cgp-cnn
```

To verify the Python version and environment setup:
```sh
python --version
```

Check if PyTorch can use a GPU and check the number of CPU cores available:
```sh
python -c "import os; print(os.cpu_count()); import torch; print(torch.cuda.is_available())"
```

### Makefile Commands

```sh
make lint
make clean_linux
make generate_package
make generate_documentation
make install
make publish
make mlflow
```

### Makefile Commands for Windows (using `mingw32-make`)

```sh
mingw32-make lint
mingw32-make clean_windows
mingw32-make generate_package
mingw32-make generate_documentation
mingw32-make install
mingw32-make publish
mingw32-make mlflow
```

### SLURM Commands

https://docs.cyfronet.pl/display/~plgpawlik/Athena

```sh
module list
module avail
module load Python/3.10.4
module unload Python/3.10.4
module spider
module spider python
module spider Python/3.11.5

sinfo
scontrol show partition
scancel 873986
sbatch job.sh
squeue
scontrol show job

hpc-grants
hpc-fs
hpc-jobs
hpc-jobs-history

source ~/athena_env/bin/activate
chmod +x script.py script.sh
!!!! UTF-8 UNIX
du -sh $HOME/*
du -h --max-depth=1 $HOME
rm -rf $HOME/.cache/*
rm -rf logs/error_*.txt logs/result_*.txt
``` 

## Usage

To ensure an easy introduction to the library, all examples that can be quickly executed are provided as Jupyter notebooks located in the `notebooks` directory. These notebooks are designed to demonstrate the functionality of the framework and guide you through the process of optimizing CNNs using Cartesian Genetic Programming.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/MrLipa/CGP-CNN-Optimizer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/MrLipa/CGP-CNN-Optimizer/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/MrLipa/CGP-CNN-Optimizer/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/MrLipa/CGP-CNN-Optimizer/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/MrLipa/CGP-CNN-Optimizer/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/tomasz-szkaradek/
