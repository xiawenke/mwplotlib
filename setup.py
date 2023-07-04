from gettext import install
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mwplotlib",
    version="1.1.3",
    author="Wenky",
    author_email="wxia1@fandm.edu",
    description="The Milky Way Plotting Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xiawenke/mwplotlib",
    packages=setuptools.find_packages(),
    install_requires=[
        "astropy",
        "numpy",
        "pandas",
        "matplotlib"
    ],
    package_data={
        'mwplotlib': [
            'data/*.txt'
        ]
    }
)