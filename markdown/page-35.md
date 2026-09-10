# Schedules

# Purpose

Schedules automatically update a participant’s haptic feedback range using recent sensor data. When a schedule is due, the system calculates the average, median, or mode (most common value). It then creates a range below and above this value using the selected percentage. This allows the feedback range to adapt without manual updates.

A schedule defines:

- which participant to check;
- how often the check runs;
- how the participant’s recent data is calculated, using the average, median, or most common value;
- how much the vibration trigger should change.

This is useful when haptic feedback needs to adapt to new participant data during a study. Without a schedule, the researcher would need to review the data and update the settings manually.

# Example

A schedule runs every seven days and uses the average value with a range of 20%. If the participant’s average is 100, the new feedback range is 80–120. The next update is planned for seven days later.

# What a schedule includes

| Field | Meaning |
| --- | --- |
| `schedule_id` | Automatically generated schedule identifier. |
| `user_id` | The user the schedule applies to. |
| `interval_days` | The number of recent days used for the calculation. It also controls when the next update runs. |
| `next_run_date` | The next scheduled run date. |
| `measure_type` | Calculation method: `average`, `median`, or `mode`. |
| `trigger_percentage` | The size of the range below and above the calculated value. |
| `active` | Whether the schedule is enabled. |

# How schedule management works

1. A request arrives with an action, parameters, session ID, and use-case context.
2. The request is parsed and checked.
3. Values are converted into the expected data types.
4. `next_run_date` is calculated from today plus `interval_days`.
5. The requested action is routed to the matching database operation.

# Supported actions

| Action | Description |
| --- | --- |
| `add` | Creates a new active schedule. |
| `change` | Updates interval, measure type, trigger percentage, or user. |
| `deactivate` | Disables a schedule. |
| `activate` | Re-enables a schedule. |
| `listAll` | Lists all schedules for the use case. |
| `listActive` | Lists active schedules only. |

# Where researchers can use schedules

Schedules can be managed from the ResearcherSideApp schedule area and through the AI assistant.