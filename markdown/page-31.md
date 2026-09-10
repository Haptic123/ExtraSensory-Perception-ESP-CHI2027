# ResearcherSideApp Configuration

# Purpose

This page explains the technical configuration points for maintaining the ResearcherSideApp.

# Database configuration

The dashboard must connect to the same database environment used by the backend workflows for the current study.

Check:

- Database host.
- Database name.
- Username and password.
- Port.
- Environment type: local, staging, or active study.

# Backend configuration

If the dashboard calls backend endpoints, make sure endpoint URLs match the active n8n environment.

# Common configuration issues

| Issue | Likely cause |
| --- | --- |
| App starts but no users appear | Wrong database or missing records. |
| Rule changes do not affect feedback | Dashboard and backend are using different databases. |
| Assistant actions fail | Backend workflow unavailable or incorrect endpoint. |
| Data views are empty | No data recorded or wrong filter/use case. |

# Safe configuration process

1. Update configuration in a test environment first.
2. Start the app.
3. Confirm users and mappings appear.
4. Run a small test action.
5. Confirm backend and database results match.