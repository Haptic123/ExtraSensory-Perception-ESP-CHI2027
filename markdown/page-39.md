# Smartwatch Haptic Command Handling

# Purpose

This page explains how the smartwatch receives and performs haptic feedback commands.

# Haptic command fields

The smartwatch receives commands that may include:

| Field | Meaning |
| --- | --- |
| `pulses` | Number of vibration pulses. |
| `intensity` | Vibration strength. |
| `duration` | Length of each pulse. |
| `interval` | Time between pulses. |
| `min value` | Minimum response parameter value the vibration can trigger from |
| `max value` | Maximum response parameter value the vibration can trigger from |

# Runtime flow

1. The smartwatch reads a body-sensor value, such as heart rate.
2. The watch sends the reading to the Android phone.
3. The phone adds identifiers and context, then sends the request to n8n.
4. n8n resolves the user's active mapping through `User_UC_Mappings -> feedback_config_rules -> UseCase`.
5. n8n applies the mapping, stores the reading and feedback decision, and returns a haptic command.
6. The phone relays the command to the watch.
7. The watch vibrates.

# What to check when vibration feels wrong

- Whether the command includes all required fields.
- Whether intensity or duration is too low to notice.
- Whether the watch is in a state that allows vibration.
- Whether the expected mapping rule was used by the backend.