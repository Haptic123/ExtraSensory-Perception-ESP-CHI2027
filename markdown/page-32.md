# ResearcherSideApp Troubleshooting

# Purpose

This page lists common ResearcherSideApp issues and how to investigate them.

# App does not start

Check:

- JDK 17 is installed.
- Build command completes.
- Configuration is valid.
- n8n is running
- Database is running.
- Database credentials are correct.

# Users are missing

Check:

- n8n executions have no failed ones
- Correct database environment.
- User table has records.
- DB Manager workflow, if the dashboard depends on backend endpoints.
- Filters in the dashboard.

# Rule changes do not affect vibration

Check:

- Rule is active.
- Rule type matches the use case exactly.
- Incoming values fall inside the rule range.
- There is no participant-specific rule overriding the global rule.
- Backend workflows use the same database as the dashboard.

# Assistant action fails

Check:

- Request includes required details.
- Relevant backend workflow is active.
- Use-case name is correct.
- Schedule ID, user ID, or mapping values are included when required.

# Escalation checklist

When reporting an issue, include:

- App version or build date.
- Database&n8n environment.
- User/use-case being tested.
- What action was attempted.
- Error message or screenshot.
- Whether backend executions show an error.