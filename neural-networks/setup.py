# -*- coding: utf-8 -*-

from gettext import install
import  setuptools

if __name__ == "__main__":
    setuptools.setup(
        name = "neural-network",
        version = "0.1.0",
        package_dir= {"": "src"},
        packages = setuptools.find_packages(),
        author = "David Landa",
        install_requires = [
            "numpy",
            "tqdm"
        ]
    )
