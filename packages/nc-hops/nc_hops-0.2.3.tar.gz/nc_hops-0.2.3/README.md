# Hops File Reader and Writer

## Overview

The `Hops File Reader and Writer` package is a Python library designed to facilitate the reading and writing of `.hop` files. These files are primarily associated with Hops, a Computer-Aided Manufacturing (CAM) software predominantly used with HolzHer CNC machines. Additionally, `.hop` files are compatible with other CNC machines from manufacturers like Homag and Ima.

## Installation

To install this package, ensure that you have a virtual environment activated. Navigate to the directory containing the `setup.py` file and execute the following command:

```bash
python -m pip install .
```

## Usage

### Reading .hop Files
- Extract various elements such as VARS, comments, and processing details from .hop files.

### Writing .hop Files
- Utilize the `WriteHop` module to create .hop files.
- Current writing capabilities include modules for Milling, Drilling, Machine, and Nesting operations.

## Roadmap

This is an ongoing project with the immediate goal of integrating all milling and drilling macros into their respective modules. Further enhancements and features will be continuously developed.

## Author

Nikola Brajic

## License

This project is currently not licensed.

## Project Status

Ongoing - The project is actively being developed, with updates and improvements made regularly.
