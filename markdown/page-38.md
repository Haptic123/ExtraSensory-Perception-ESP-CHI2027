# Smartwatch App Overview

# Purpose

This page explains the smartwatch app in practical terms for researchers preparing or running a participant session.

# What the smartwatch app does

The smartwatch app is the participant-facing part of the system. It collects physiological or sensor data, communicates with the Android phone relay, and delivers haptic feedback through vibration.

# Main responsibilities

- Collect sensor data such as heart rate.
- Send watch-side data to the phone relay.
- Receive vibration commands from the phone.
- Translate haptic commands into physical vibration patterns.
- Continue running during a study session using foreground/background support.

# Researcher responsibilities

Before a session, confirm that:

- The watch is charged.
- The app is installed.
- The required permissions are granted.
- The watch name follows the expected naming format.
- The watch can communicate with the phone.
- A simple test reading and test vibration work as expected.

# When to check this app

Check the smartwatch app if:

- Heart rate or sensor values are missing.
- The phone does not receive watch data.
- The backend returns feedback but the participant does not feel a vibration.
- The watch disconnects during a session.