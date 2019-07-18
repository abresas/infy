from setuptools import setup, find_packages

setup(
    name="infy",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'kivy>=1.11.0',
        'parsimonious>=0.8.1',
        'pint>=0.9',
        'plyer>=1.4.0',
    ],
    entry_points={
    },
    author="Alexios Brezas",
    author_email="abresas@gmail.com",
    keywords="math notes editor kivy",
    url="https://github.com/abresas/infy",
    project_urls={
        "Bug Tracker": "https://github.com/abresas/infy/issues",
        "Source Code": "https://github.com/abresas/infy",
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
