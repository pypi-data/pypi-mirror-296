from setuptools import setup, find_packages

setup(
    name="zipschema",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "pyyaml",
        "jsonschema",
        "jinja2"
    ],
    entry_points={
        'console_scripts': [
            'zipschema=zipschema.zipschema:cli',
            'zs=zipschema.zipschema:cli'
        ],
    },
    author="Your Name",
    description="CLI tool for validating zipschema files and generating documentation.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mrmessagewriter/zipschema",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
