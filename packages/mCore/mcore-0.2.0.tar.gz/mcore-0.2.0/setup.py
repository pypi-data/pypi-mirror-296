"""
    Setup file for mCore.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.5.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup, find_packages

if __name__ == "__main__":
    try:
        setup(
            use_scm_version={"version_scheme": "no-guess-dev"},
            version='0.2.0',
            package_dir={'': 'src'},  # Indique que les packages sont dans 'src'
            packages=find_packages(where='src'),  # Recherchez les packages dans 'src/mCore'
            include_package_data=True,  # Inclut les fichiers non-Python si MANIFEST.in est présent
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
