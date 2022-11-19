# MCtech Cosmic Ray Detector

<!-- [![License](https://img.shields.io/pypi/l/mctech-crd)][license] -->

Python package for a Raspberry Pi Cosmic Ray detector.

Designed to work with the 'Cosmic Pi' hardware from Mayes Creative Technology.

The code will handle input from the hardware sensor that records a 'hit' from a cosmic ray.

It then logs and translates this into various outputs based on configuration.

See the docs for a [full list of features](docs/features.md).

# Requirements

Raspberry Pi running Python 3.

A monitor and audio outputs if using the media player.

## Installation

A Raspberry pi provided from MC Technology will already include the cosmic
package, which should run automatically on boot.

If you are starting with an existing Pi, or an older 'Cosmic Pi'  prior to
automatic updates, see [Setting up an existing Pi as a Cosmic Ray Detector](docs/setup_existing_pi.md)

# Usage

The `cosmicservice` will run automatically in the background.

See `cosmic --help` on the Cosmic Pi for details of command line usage.

## Credits

This project was instigated by MC Technology.

The initial code for this project was written by [glenpike](https://github.com/glenpike).

Additions and development of the python package and Raspberry Pi image by
[tombola](https://github.com/tombola).

[license]: https://github.com/MC-Technology/mctech-crd/blob/main/LICENSE
[hypermodern python cookiecutter]:
    https://github.com/cjolowicz/cookiecutter-hypermodern-python

## License

_This project is licensed under [GPLv3](LICENSE)._