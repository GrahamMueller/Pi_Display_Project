#!/bin/bash

export DISPLAY=:0.0
#Runs the command as the user in tty7, which is likely the default logged in user.
python3 active_display/active_pi_display.py -f /dev/tty7