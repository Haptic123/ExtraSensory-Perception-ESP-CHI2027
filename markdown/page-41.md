# Smartwatch Troubleshooting

# Purpose

This page lists common smartwatch app issues and how to investigate them.

# No sensor data

Check:

- Body Sensors permission.
- Watch placement on the wrist.
- Whether the app is running.
- Whether the foreground service is active.
- Watch battery and power-saving state.

# Watch cannot communicate with the phone

Check:

- Bluetooth enabled on both devices.
- Phone app is running.
- Watch app is running.
- Device naming is correct.
- Nearby Devices/Bluetooth permissions are granted.

# Watch receives command but does not vibrate

Check:

- Command includes pulses, intensity, duration, and interval.
- Intensity and duration are noticeable.
- Watch vibration settings are enabled.
- The app is allowed to run in the background.

# Useful logs

Use Android Studio Logcat for watch-side debugging. Look for sensor registration, Bluetooth connection, incoming command, and vibration execution messages.

# Escalation checklist

When reporting a smartwatch issue, include:

- Watch model.
- Wear OS version.
- App version or build date.
- Phone model.
- Participant/user ID used for testing.
- What was expected to happen.
- What actually happened.