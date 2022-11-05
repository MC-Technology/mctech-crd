# MCtech Cosmic Ray Detector

[![PyPI](https://img.shields.io/pypi/v/mctech-crd.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/mctech-crd.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/mctech-crd)][python version]
[![License](https://img.shields.io/pypi/l/mctech-crd)][license]

[![Read the documentation at https://mctech-crd.readthedocs.io/](https://img.shields.io/readthedocs/mctech-crd/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/MC-Technology/mctech-crd/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/tombola/mctech-crd/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/mctech-crd/
[status]: https://pypi.org/project/mctech-crd/
[python version]: https://pypi.org/project/mctech-crd
[read the docs]: https://mctech-crd.readthedocs.io/
[tests]: https://github.com/MC-Technology/mctech-crd/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/tombola/mctech-crd
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

Python package for a Raspberry Pi Cosmic Ray detector.

Designed to work with the Mayes Creative Tech Cosmic Pi 'hardware'.

The code will handle input from the hardware sensor that records a 'hit' from a cosmic ray.

It then translates this into various outputs based on configuration.

# Requirements

Raspberry Pi running Python 3.

A monitor and audio outputs if using the media player.

## Installation

You can install _MCtech Cosmic Ray Detector_ via [pip] from GitHub, using a [pat].

```console
$ pip install git+https://{token}@github.com/MC-Technology/mctech-crd.git@{version}

```

## Features

- TODO

## Usage

Please see the [Command-line Reference] for details.

# Setup

Clone this repository and change directory into the cloned folder.

Install the requirements with `pip3 install -r requirements.txt`

Run the programme with `python3 src/cosmic.py -h` to see arguments

## Run at startup

Add the following line to the file `/etc/rc.local`:

```
su pi -c '/home/pi/cosmic-pi/launcher.sh
```

This will run the launcher script as the pi user (so that it uses the above installed python libs)

If you run this script at startup, there is possibly an issue where the GPS sensor is not ready before the code runs and it may exit (TO BE FIXED)

# Configuration

The software will default to using the [config/dev.yaml](config/dev.yaml) file to configure itself. This allows various modules to be switched on and configured, e.g.

```yaml
location: SE10 8XJ
media_player: true
google_logging:
  sheet_id: 1234abcde
  credentials_file: development
text_logging: true
gps_sensor: true
servo_motor: true
midi_controls:
  sensitivity: 10
  sensitivity_seconds: 10
  servo_angle: 11
  angle_multiplier: 90
  servo_on_ctrl: 91
  servo_on_time: 1
relay_output:
  gpio_pin: 24
  on_time: 6
switch_input:
  gpio_pin: 23
```

## Media Player

Set `media_player: true` to enable the playback of video files that are stored in /home/pi/video and /home/pi/audio
The playback is currently hardcoded to play specific files from the original Cosmic Pi code.
See [src/media_player.py](src/media_player.py)

## Google Logging

```yaml
google_logging:
  sheet_id: 1234abcde
  credentials_file: development
```

To log detection events to a Google Spreadsheet you will need to

1. [create a service
   account](https://cloud.google.com/docs/authentication/production#create_service_account)
   for this raspberrypi in the google console with editor role
2. Share the google sheet with the new service account (use the email address
   listed in service accounts)
3. create a credentials JSON file representing the service account (see 'keys' tab
   on the service account)
4. add the credentials JSON file to the ./credentials directory
5. reference it as `credentials_file` in the config file: e.g. (see above example)

You will also need the id of the spreadsheet you are logging to - this is in the URL usually, so: https://docs.google.com/spreadsheets/d/1234abcde/edit#gid=0 would give you the id in the example above.

See [src/google_sheets.py](src/google_sheets.py)

## Text Logging

Set `text_logging: true` to enable logging of hits to a text file. This will be
sent to a file called 'cosmic_pi_event.log' in `/home/.cosmic/tmp`.

## Location

Use the postcode where the device will be for setting the location that is logged using either of the systems above, e.g.
`location: SE10 8XJ`

## GPS Sensor

Requires the SixFab Sensor hat hardware attached, with the GPS aerial and the device will need to be located where it can have a visual line to satellites, e.g. outside.

Set `gps_sensor: true` - this will enable the GPS location of the setup to be added to the log. If this is enabled, but not present, (or disabled) the system will fallback to the configured location above
See [src/sixfab_sensors.py](src/sixfab_sensors.py)

## Servo Motor

A servo motor can be plugged into the GPIO - using GPIO 17 - and this will move when the system records a hit from a cosmic ray.
Set `servo_motor: true` to enable this.

## Midi Controls

To 'fake' cosmic ray hits in experimental situations and controlling the servo motor, you can plugin a Midi control device.

```yaml
midi_controls:
  sensitivity: 10
  sensitivity_seconds: 10
  servo_angle: 11
  angle_multiplier: 90
  servo_on_ctrl: 91
  servo_on_time: 1
```

Note On from the device is used to simulate a hit, and 3 continuous controllers can be used to adjust:

Sensitivity - how long the system waits after a cosmic ray hit before responding to the next one (in case it is quite a busy day)

`sensitivity_seconds` will be the maximum number of seconds you can set this to
`sensitivity` is the number of the Midi CC that will adjust this.

Servo Angle - where the servo moves to when a hit is recorded

`angle_multiplier` controls the amount of rotation
`servo_angle` is the Midi CC adjusting it.

Servo Duration - how long the servo remains at the above angle after a hit.

`servo_on_time` - maximum time
`servo_on_ctrl` - Midi CC control

## Relay Output

When a hit is detected, it will switch on a relay on the configured pin for a number of seconds

`gpio_pin` - the pin that will be switched on when a hit is detected (default 24)
`on_time` - the number of seconds that the pin will be switched on for (default 6 seconds)

## Switch Input

Another way of faking hits using a switch that connects the configured pin to ground

`gpio_pin` - the pin that the switch is connected to.
## Service

The cosmic listener starts at boot as a background service. It can be monitored
and managed as follows:

```
sudo systemctl status cosmicservice
sudo systemctl start cosmicservice
sudo systemctl stop cosmicservice
sudo systemctl restart cosmicservice

# To check if the service is running
sudo systemctl is-active --quiet cosmicservice && echo "running" || echo "not running"
```


## Credits

The initial code for this project was written by [glenpike](https://github.com/glenpike).

This python package structure was initially generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/MC-Technology/mctech-crd/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/MC-Technology/mctech-crd/blob/main/LICENSE
[contributor guide]: https://github.com/MC-Technology/mctech-crd/blob/main/CONTRIBUTING.md
[command-line reference]: https://mctech-crd.readthedocs.io/en/latest/usage.html
[pat]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
