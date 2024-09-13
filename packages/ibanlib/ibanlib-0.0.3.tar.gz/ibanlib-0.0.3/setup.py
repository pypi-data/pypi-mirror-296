from setuptools import setup, find_packages

setup(
    name = "ibanlib",
    version = "0.0.3",
    description="Library that supports developing applications that integrate the International Bank Account Number (IBAN).",
    author = "Hermann Himmelbauer",
    author_email = "hermann@himmelbauer-it.at",
    license = 'LGPL',
    packages = find_packages(),
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.cfg'],
    }
)

