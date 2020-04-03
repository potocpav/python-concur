
<h1 align="center">
  Python Concur
</h1>

<p align="center">
   <img src="https://raw.githubusercontent.com/ajnsit/purescript-concur/master/docs/logo.png" height="100">
</p>

[![Build Status](https://travis-ci.com/potocpav/python-concur.svg?branch=master)](https://travis-ci.com/potocpav/python-concur)

* [**Documentation**](https://potocpav.github.io/python-concur-docs/master/)
* [**Homepage**](https://potocpav.github.io/python-concur-docs/homepage.html)
* [Examples](https://github.com/potocpav/python-concur/tree/master/examples)
* [PyPI](https://pypi.org/project/concur/)
* [Changelog](https://github.com/potocpav/python-concur/tree/master/CHANGELOG.md)

<!-- Start docs -->

Concur is a Python UI framework based on synchronous generators.

It is a port of [Concur for Purescript](https://github.com/ajnsit/purescript-concur), implemented on top of the [Dear ImGui](https://github.com/ocornut/imgui) C++ UI library.

For introduction to core concepts, see the [documentation](file:///home/pavel/build/python-concur/docs/index.html#introduction). A more comprehensive introduction can be found in the [Documentation for the Haskell/Purescript versions](https://github.com/ajnsit/concur-documentation/blob/master/README.md). This obviously uses Haskell/Purescript syntax and semantics, but many of the concepts will apply to the Python version.

Being an abstraction over ImGui, Concur is best used for debugging, prototyping and data analysis, rather than user-facing applications. ImGui functions can be used directly for any functionality that is not wrapped by Concur. See the [PyImGui docs](https://pyimgui.readthedocs.io/en/latest/) for additional widgets, or [ImGui itself](https://github.com/ocornut/imgui) if you need to poke really deep.

<!-- End docs -->


## Installation

The only dependencies are a C++ compiler, [GLFW](https://github.com/glfw/glfw) and Python >= 3.6. Concur [is available on PyPI](https://pypi.org/project/concur/) and can be installed using pip:

```sh
pip install concur
```

This command should produce a very simple GUI app:

```sh
python -c 'import concur as c; c.main("Hello", c.button("Close"), 500, 500)'
```

Use any of the [examples](https://github.com/potocpav/python-concur/tree/master/examples) as a starting point for your app.

## Development

For Concur development, clone the repo and install it using pip:

```sh
git clone https://github.com/potocpav/python-concur.git
cd python-concur
pip install -e.

examples/all.py # Run the examples to verify installation
```

To run the tests, you need PyTest and PyTest-benchmark:

```sh
pip install pytest pytest-benchmark

pytest # Run the tests
```

To build documentation, install [pdoc3](https://pdoc3.github.io/pdoc/) (`pip install pdoc3`), clone the submodules (`git submodule update --init`), and run the script `./mkdocs.sh`.


<p align="center">
<img src="https://raw.githubusercontent.com/potocpav/python-concur-docs/master/screenshot.png">
</p>
