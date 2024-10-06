import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="concur",
    version="0.11.0",
    author="Pavel Potocek",
    author_email="pavelpotocek@gmail.com",
    description="Concur UI Framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://potocpav.github.io/python-concur-docs/homepage.html",
    project_urls={
        "Documentation": "https://potocpav.github.io/python-concur-docs/master",
        "Source Code": "https://github.com/potocpav/python-concur",
        "Bug Tracker": "https://github.com/potocpav/python-concur/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        "Topic :: Software Development :: User Interfaces",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.6',
    install_requires=[
        'imgui >= 2.0.0',
        'Pillow',
        'numpy',
        'glfw',
        'PyOpenGL',
        'imageio',        # Only needed for render-to-video
        'imageio-ffmpeg'  # Only needed for render-to-video
    ],
)
