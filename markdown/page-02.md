# Phone and Watch Connection

Use this page when the watch and phone are not communicating reliably.

# What should happen

The smartwatch sends readings to the phone over Bluetooth. The phone sends haptic commands back to the watch over the same local connection path.

# Things to check

- Bluetooth is enabled on the phone.
- The smartwatch app is running.
- The watch is named correctly.
- The phone is paired with or able to discover the watch.
- The phone app is not connected to the wrong watch.
- The watch has not gone into a state where the app stopped running.

# Common symptoms

- Data is visible on the watch but not in the backend.
- n8n returns a haptic instruction but the watch does not vibrate.
- The phone appears disconnected or stops receiving watch messages.

# What to try

- Restart the watch app.
- Restart the phone app.
- Reconnect Bluetooth.
- Confirm the phone is using the intended participant/watch pair.