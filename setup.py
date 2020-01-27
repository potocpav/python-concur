import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="concur",
    version="0.3.0",
    author="Pavel Potocek",
    author_email="pavelpotocek@gmail.com",
    description="Concur UI Framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/potocpav/python-concur",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        "Topic :: Software Development :: User Interfaces",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.6',
    install_requires=[
        'concur-imgui >= 1.2.1',
        'Pillow',
        'numpy',
        'glfw',
        # PyOpenGL is pinned to 3.1.0, due to the issue of glGenTextures() intermittently failing after
        # commit https://github.com/mcfletch/pyopengl/commit/ed0ca79b981663c4697c3b2792eec176dd4f4121
        # The issue is reproducible when dragging the image in `examples/image.py`, and manifests as
        # image flicker and intermittent crashes.
        # This bug is reproducible also in `PyOpenGL==3.1.0`, when `glGenTextures` is used to generate
        # multiple textures at once.
        'PyOpenGL == 3.1.0',
    ],
)
