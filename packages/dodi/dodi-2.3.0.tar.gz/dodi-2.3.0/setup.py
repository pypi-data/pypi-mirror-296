import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION', 'r') as fh:
    version = fh.read()

setuptools.setup(
    name="dodi",
    version=version,
    author="Alex Fischer",
    author_email="alex@quadrant.net",
    description="Django On-Demand Images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="TODO - github repo",
    packages=['dodi'],
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["Django>=2.2,<5", "Pillow>=7.0.0,!=7.2.*,!=8.0.*,!=8.1.*,!=8.2.*,<10"],
)