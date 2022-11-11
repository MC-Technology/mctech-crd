## Setting up an existing Pi as a Cosmic Ray Detector

Requirements:

- `mct_credentials` folder (provided by MC Technology)
- raspberry pi image (provided by MC Technology)
- storage media (sd card/usb stick) for use on the Pi

Initialising CRD:

- **on your computer:**
  -  Use the [raspberry pi
      imager](https://www.raspberrypi.com/news/raspberry-pi-imager-imaging-utility/)
      to write the provided image to your card/stick
      - select 'custom image' and find the image
      - in the imager settings (see cog icon)
          - add your wifi credentials
          - leave the user as `cosmic`
          - uncheck 'Eject media when finished'
      - write
    - copy the provided `mct_credentials` folder to the `boot` drive\*
    - eject media
- **on the Raspberry Pi:**
    - insert media, power on and allow time to boot and initialise
- **from your computer:**
    - resize the partition to fill disk
      `ssh cosmic@cosmic.local sudo raspi-config --expand-rootfs && sudo shutdown -r now`
        - when prompted, default password is cosmic

On reboot the Pi should now display the message `Cosmic detection service is
running`.
You can check the client version matches latest release with `cosmic version --latest`.

The Pi should pick up new releases of the software when it reboots.