# Cosmic Pi

Raspberry Pi + Cosmic Ray detector

This project contains Python code that will work with the Mayes Creative Cosmic Pi 'hardware'.

The code will handle input from the hardware sensor that records a 'hit' from a cosmic ray.

It then translates this into various outputs based on configuration.

# Requirements

Python 3

A monitor and audio outputs if using the media player.

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
location: TR11 3PH
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

Set `text_logging: true` to enable logging of hits to a text file. This will be sent to a file called 'cosmic_pi_event.log' in this directory
See [src/text_event_writer.py](src/text_event_writer.py)

## Location

Use the postcode where the device will be for setting the location that is logged using either of the systems above, e.g.
`location: TR11 3PH`

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
