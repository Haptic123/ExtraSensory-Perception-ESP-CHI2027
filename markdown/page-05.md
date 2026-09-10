# Phone App Troubleshooting

# Purpose

This page lists common Android phone app issues and how to investigate them.

# Data is not reaching the backend

Check:

- Backend IP/domain.
- Phone network connection.
- Whether the backend is running.
- Whether the correct webhook path is used.
- Whether the workflow is active.
- Android network security settings.

# Watch does not vibrate

Check:

- Backend response includes haptic parameters.
- Phone receives the response.
- Phone is connected to the watch.
- Watch app is running.
- Watch permissions are granted.

# Phone cannot connect to watch

Check:

- Bluetooth enabled on both devices.
- Pairing state.
- Watch app running.
- Phone app running.
- Nearby Devices/Bluetooth permissions.

# Useful logs

Use Android Studio Logcat to inspect app behavior. Look for network errors, Bluetooth connection errors, and backend response messages.

# Escalation checklist

When reporting a phone app issue, include:

- Phone model.
- Android version.
- App version or build date.
- Backend host used.
- Watch model.
- What action was being tested.
- Any Logcat error messages.