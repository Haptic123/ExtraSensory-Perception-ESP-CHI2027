# Phone App Overview

# Purpose

This page explains the Android phone app in practical terms for researchers preparing or running a study.

# What the phone app does

The phone app is the communication bridge between the smartwatch and the backend. It receives data from the watch, adds phone-side context when needed, sends requests to the backend, and relays haptic instructions back to the watch.

# System flow

```
Smartwatch → Android phone → n8n backend → Android phone → Smartwatch
```

# Researcher responsibilities

Before a session, confirm that:

- The phone app is installed.
- Bluetooth is enabled.
- The phone can reach the internet or local backend server.
- The app is configured with the correct backend address.
- The phone can communicate with the watch.
- The watch and phone are assigned to the correct participant.

# When to check this app

Check the phone app if:

- Data is not reaching the backend.
- The watch is collecting data but not receiving feedback.
- The backend returns feedback but the watch does not vibrate.
- The phone was moved to a different network or lab setup.