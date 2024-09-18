from setuptools import setup, find_packages

setup(
    name="windrak",
    version="0.1.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "click",
        "groq",
        "python-dotenv",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "windrak=windrak.cli:cli",
        ],
    },
)