from setuptools import setup

with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="optschedule",
    version="1.0.0",
    description="Flexible parameter scheduler that can be implemented with proprietary and open source optimizers and algorithms.",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/draktr/optschedule",
    author="draktr",
    license="MIT License",
    packages=["optschedule"],
    python_requires=">=3.6",
    install_requires=["numpy"],
    keywords="schedule, optimization, decay, learning, parameters, training",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    project_urls={
        "Documentation": "https://optschedule.readthedocs.io/en/latest/",
        "Issues": "https://github.com/draktr/optschedule/issues",
    },
)
