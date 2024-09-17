from setuptools import setup, find_packages

setup(
    name="datatui",
    version="0.0.2",
    packages=find_packages(),
    install_requires=["diskcache", "textual", "srsly", "click"],
    package_data={
        "datatui": [
            "static/app.css"
        ]
    },
)
