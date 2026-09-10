# Database Functions and Views

# Purpose

This page explains the main database functions and views used by the system.

# `insert_sensor_data(...)`

This function stores a sensor reading together with the haptic alert generated for it.

It is responsible for:

1. Checking that the incoming use case matches the user’s active use case.
2. Registering user, watch, or phone records if needed.
3. Linking the user, watch, and phone.
4. Creating an alert record.
5. Creating the matching sensor data record.

# `resolve_fb_range(_userid, _sensorname, _value)`

This function finds the haptic mapping rule that should be used for a measured value.

Rule priority:

1. Use a participant-specific rule if one exists.
2. Otherwise use a global active rule.
3. Return no rule if no matching range exists.

# `touch_updated_at()`

This trigger helper updates timestamps when rows are changed.

# `v_agent_context`

This view prepares useful context for assistant responses. It combines session information, use-case information, and active mapping information.