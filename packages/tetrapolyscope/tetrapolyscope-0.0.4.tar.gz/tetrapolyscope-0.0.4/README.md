# polyscope-py
Python bindings for TetraPolyscope - Chromalab Version. TetraPolyscope is a fork of Nicholas Sharpe's [Polyscope](https://polyscope.run/py).


This library is a python wrapper and deployment system. The core library/C++ backend lives at [this repository](https://github.com/i-geng/polyscope)

### Installation

#### Install from [PyPI](https://pypi.org/project/tetrapolyscope/).

Use this installation method if you just want to use TetraPolyscope and don't need to add new functionality.

```
pip install tetrapolyscope
```

#### Local Installation

This method requires you to build the C++ backend, but is useful for development and rapid testing.

Uninstall current version of tetrapolyscope from current virtual environment:
```
pip uninstall tetrapolyscope
```

Local installation.
```
git clone --recurse-submodules git@github.com:i-geng/polyscope-py.git
```

From the root polyscope-py directory, build the C++ source:
```
mkdir build; cd build
cmake ../
make -j4
```
Back in the root polyscope-py directory:
```
pip install .
```

To use polyscope's functions for writing videos, you will also need FFmpeg.

### Publishing a New Version of TetraPolyscope

Follow documentation [here](https://polyscope.run/about/contributing/#python-bindings) and [here](https://github.com/nmwsharp/polyscope-py/blob/master/README.md) to use Github Workflow Actions.

- 9/16/24: Unit tests for macOS, Windows, and Linux builds under worklow actions are currently broken after renaming polyscope to tetrapolyscope (needed different name for PyPI upload). Can probably fix this by renaming directory names, but it doesn't affect the PyPI upload and publishing process.
