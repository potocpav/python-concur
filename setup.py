import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="concur",
    version="0.1.0",
    author="Pavel Potocek",
    author_email="pavelpotocek@gmail.com",
    description="Concur UI Framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/potocpav/python-concur",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'imgui @ git+https://github.com/potocpav/pyimgui.git',
        'Pillow',
        'numpy',
        'glfw',
        'PyOpenGL',
    ],
)
