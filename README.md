# Tasmota Power Strip Plugin

This is a plugin for the OctoPrint 3D printing software that allows users to control a Tasmota-powered power strip through the OctoPrint interface.

## Requirements

- OctoPrint version 3 or higher
- Tasmota firmware installed on a power strip (Nous AT5)
- Internet connectivity for the Raspberry Pi running OctoPrint and the Tasmota power strip

## Installation

1. Clone this repository or download the `tasmota_power_strip_plugin.py` file
2. Place the file in the `plugins` directory of your OctoPrint installation
3. Restart OctoPrint

## Configuration

1. In the `tasmota_power_strip_plugin.py` file, update the `IP` variable with the IP address of your Tasmota power strip.
2. Optional: Modify the channel mapping in the `set_channel` function to match the devices connected to your power strip. By default, the following mapping is used:
  - Ch1: Raspberry Pi
  - Ch2: 3D Printer
  - Ch3: Filter Fan
  - Ch4: Lights (USB 5V)

## Usage

Upon installation and configuration, the plugin will automatically turn on the 3D printer and turn off the filter fan upon startup.

During a print, the plugin will turn on the filter fan and lights. Upon completion of the print, the plugin will turn off the printer, filter fan, and lights after a 5 minute delay. The Raspberry Pi running OctoPrint will also be turned off after this delay.
