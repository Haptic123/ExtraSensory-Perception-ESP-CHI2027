# Smartwatch Sensor Management

# Purpose

This page explains how smartwatch sensors are handled and how new sensor types can be added.

# Current sensing role

The smartwatch collects sensor values needed by the study and sends them through the phone relay. Heart rate is a central example, but the system can be extended to support additional watch sensors.

# Adding a new watch sensor

General process:

1. Identify the Wear OS sensor type.
2. Register the sensor in the app’s sensor registry.
3. Choose a clear sensor/use-case name.
4. Make sure the phone relay and backend use the same name.
5. Add or update dictionary entries for the new use case.
6. Add haptic mappings if the sensor should trigger feedback.
7. Test with one watch before using it in a study.

# Naming consistency

The sensor name used by the watch, phone, backend, database, and researcher dashboard must match. Inconsistent naming is a common cause of missing data or missing feedback.

# Testing a new sensor

- Confirm raw values are available on the watch.
- Confirm the phone receives the values.
- Confirm the backend receives the expected use-case name.
- Confirm data is saved.
- Confirm feedback is generated only when expected.