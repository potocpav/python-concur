
# Python Concur

[Concur UI Lib](https://github.com/ajnsit/concur) is a brand new UI framework that explores an entirely new paradigm. It does not follow FRP (think Reflex or Reactive Banana), or Elm architecture, but aims to combine the best parts of both. This repo contains the Concur implementation for Python, using the PyImGui library as a backend.

## Documentation

For now, there is no API reference. Look at the source code.

Python-Concur uses an UI paradigm inspired by the [Purescript-Concur library](https://github.com/ajnsit/purescript-concur), but there are some differences. For composition in time, Python's synchronous generators are used instead of the `Widget` monad. All code blocks UI actions unless wrapped by the `block` function <sup>(TODO: rename)</sup> which accepts futures.

Python-Concur is built on top of [PyImGui](https://github.com/swistakm/pyimgui), which itself is a thin wrapper around the C++ library [Dear ImGui](https://github.com/ocornut/imgui). Widgets in python-concur mostly correspond one-to-one to PyImGui widgets. The main differences are:

* Containers accept children as parameters. No begin/end pairs.
* Widgets are by default composed in time, not in space. For composition in space, use the `orr` function.
* No need to uniquely name widgets, no name clashes.
* Much less spaghetti (especially in asynchronous code), at the cost of conceptual difficulty and some syntactic quirks.
