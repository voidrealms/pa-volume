# pa-volume
Pulse Audio volume control for Linux

Simple Python script using TKinter to control the volume of devices in Linux.

Goals:
Allows volume up to 200%
Easy UI
Simple script (under 100 lines)
Avoid bloat such as extra modules

Wraps the following commands:
pacmd list-sinks
pactl set-sink-volume 1 150%
