# Running and Testing Workflows

# Purpose

This page explains how to run and test n8n workflows safely before using the system with participants.

# Recommended testing process

1. Identify the workflow you need to test.
2. Use a known participant ID and device ID.
3. Run the workflow in test mode first.
4. Send a sample request.
5. Check each node output.
6. Confirm the final response.
7. Confirm the database row was created or updated when expected.

# What to inspect during a test

- Incoming request fields.
- Parsed values.
- Database query results.
- Mapping rule chosen by the workflow.
- Generated vibration parameters.
- Final webhook response.

# Common signs of a problem

| Symptom | What to check |
| --- | --- |
| Webhook does not respond | Workflow is inactive or wrong URL is used. |
| Empty database result | Wrong database credentials or missing rows. |
| Watch does not vibrate | Missing haptic parameters or phone-watch connection issue. |
| Assistant asks for clarification | Request is missing action, use case, user, or required values. |

[n8n Webhook Tests Breakdown](page-24.md)