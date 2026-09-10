# Users and Use Cases

Use this page when you need to select a participant or work with use cases in the dashboard.

# Users

A user represents a participant in the study. In the dashboard, selecting a user sets the context for mappings, schedules, graphs, and assistant/chat actions.

## Monitoring status

Each user in the **Users List** has a colored status indicator:

- 🟢 **Connected:** a request was received within the last 10 minutes.
- 🟠 **Not responding:** no request was received for more than 10 minutes.
- 🔴 **Alert sent:** IT has been notified that the user is offline.
- ⚪ **Monitoring stopped:** monitoring was intentionally stopped or is not expected.

[REMOVED FOR ANONYMITY]

Hover over the indicator to see its description.

# Use cases

A use case represents the type of signal or condition being monitored. Examples include:

- `HeartRate`
- `Pollution`
- `AirPressure`
- `UVIndex`
- `SunAzimuth`
- `MoonAzimuth`

# Selecting a user and a use case

When you select a user and use case, the dashboard should show the mappings and data relevant to that context.

The current use case is based on the participant's active mapping assignment. In practical terms, this means that changing a participant's mapping can also change what use case appears active for that participant.

# Assigning a use case to a user

To allow a user (participant) to get a vibration, you’ll need to assign a use case to them. Go to the user’s tab, select your desired user, locate the “Assign Use Case” section at the bottom, and select the use case.

# Creating a use case

Use-case names should be compact and should not contain spaces. After creating a use case, it should become available in the dashboard without requiring you to manually rebuild the page.

Full guide: [Adding a New Use Case](page-01.md)