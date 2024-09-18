# Behaverse Python Package

The `behaverse-data-loader` package is a Python implementation of the Behaverse Data, enabling seamless access to behavioral datasets in Python.

## Installation

To install the package, you can use pip:

```bash
pip install behaverse-data-loader
```

## Usage

See the [Behaverse website](https://behaverse.org/data) for more information on how to use the package.

## License

TODO

## Contributing


### Development

Before starting development, you need to install the dependencies. You can do this by creating a new conda environment as defined in the `environment.yml` file:

```bash
mamba env create -f environment.yml
mamba activate behaverse
```

### Documentation

To generate documentations and API reference, run the following commands from the main directory of the project:

```bash
cd docs
quartodoc build && quartodoc interlinks && quarto preview
```

The documentation will be available in the `docs/_site/` directory.



## Acknowledgements

TODO

## Citation

TODO
