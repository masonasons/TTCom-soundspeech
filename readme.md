# TTCom-soundspeech
Welcome to the TTCom 3.0 trigger.
This trigger attempts to backport the speech and sound changes from the TTCom 4.0 code modification fork that has very become quickly outdated to work wit the mainstream TTCom 3.0 trigger release from Doug Lee.
In addition, this trigger fixes a lot of the shortcomings the 4.0 fork itself had.

# Changes
## New in 1.11
* Fixes logged out messages. I am so stupid...
## New in 1.1
* Slightly more robust status handling code.
* Removes User from messages
* Now runs separate from TTCom (Thanks Doug).
* A surprise!

# How to install:
place ttcom_triggers.py and it's accompanying include folders in your TTCom directory.
If TTCom is already running, type refresh
Otherwise, start TTCom.

This document assumes you already know how to use TTCom, and therefore will not explain how to use TTCom.

# Features:
* Speak user events through your screen reader on Windows.
* Play sounds for user events on Windows.
* Log user events to file.

This trigger adds the following additional optional server parameters to your config file.
* speech=False: disable speech events for a specific server.
* log=False: disable text logging for a specific server.
* interrupt=True: Will this server's speech events interrupt currently existing speech? Default: False

Feel free to make code modifications to this as needed, and also feel free to throw them back at me if you feel like it.