# Phone-Watch Communication

# Purpose

This page explains the phone app’s role in Bluetooth communication with the smartwatch.

# Communication role

The phone app receives watch data and sends feedback commands back to the watch. It needs a stable Bluetooth connection for the system to work reliably.

# What the phone sends to the backend

Depending on the use case, the phone may send:

- User ID.
- Watch ID.
- Phone ID.
- Sensor value.
- Sensor or use-case type.
- Location data when required.
- Timestamp or context fields.

# What the phone receives from the backend

The backend response may include haptic parameters such as:

- `pulses`
- `intensity`
- `duration`
- `interval`
- feedback reason or status

# Troubleshooting communication

| Symptom | What to check |
| --- | --- |
| Watch data does not reach the phone | Bluetooth state, watch app state, device pairing. |
| Phone reaches backend but watch does not vibrate | Phone-watch connection and returned command format. |
| Connection is unstable | Distance, battery state, Bluetooth permissions, background restrictions. |