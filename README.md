
# Python Concur

Concur is a Python UI framework based on synchronous generators.

It is a port of [Concur for Haskell](https://github.com/ajnsit/concur) and [Concur for Purescript](https://github.com/ajnsit/purescript-concur).

Concur can be thought of as a layer on top of [PyImGui](https://github.com/swistakm/pyimgui), which is a set of bindings for the [ImGui](https://github.com/ocornut/imgui) UI library. It helps you to get rid of unprincipled code with mutable state, and lets you build structured and composable abstractions.

A discussion of Concur concepts can also be found in the [Documentation for the Haskell/Purescript versions](https://github.com/ajnsit/concur-documentation/blob/master/README.md). This obviously uses Haskell/Purescript syntax and semantics, but many of the concepts will apply to the Python version.

## Sample Code

Code samples can be found in the [examples directory](examples).

## Usage

Clone and install a PyImGui fork:

```sh
git clone git@github.com:potocpav/pyimgui.git --recurse-submodules
cd pyimgui
pip install -e.[glfw] --user
cd ..
```

Clone and install the Concur repo:

```sh
git clone git@github.com:potocpav/python-concur.git
cd python-concur
pip install -e. --user
```

Run the examples:

```sh
python examples/all.py
```

## Introduction

TODO

## Quirks and Issues

Here's a list of known issues that probably can't be fixed easily:

**Widget flicker**

Between any two `yield from _` statements that can return, there must be a `yield` statement. Otherwise, elements may get duplicated in a frame after triggering an action. If there are too many `yield` statemets, however, elements may momentarily disappear.

I don't think this bit of syntactic inconvenience can be solved without introducing other quirks.

**Event congestion**

On each frame, at most one action can get triggered from an `orr` block. Actions from first sub-widgets are prioritized, and any actions from further sub-widgets may get thrown out. This is a problem when there are rapidly-firing widgets, such as video playback. Move it down the `orr` block to decrease the priority.

This limitation can be lifted by changing the widgets to return lists of actions instead of only one action. It would make the API a bit uglier though, so I am not sold on the idea. If you have a better solution, or your use-case necessitates such change, file an issue.

**Asynchronous computations**

In other versions of Concur, all widgets are triggered asynchronously. This may not be possible in Python, due to a limitation of async generators: they can't `return` a value, they only `yield`. Synchronous generators are used instead, which means that all widget code is run in the main thread. Any asynchronous code must be explicitly run in a background thread, which is easily achieved by passing a future into the `block` function. See the [timers example](examples/timers.py) for details.
