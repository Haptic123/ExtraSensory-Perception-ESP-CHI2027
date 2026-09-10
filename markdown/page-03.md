# Phone App Configuration

# Purpose

This page explains the technical configuration points for the Android phone app.

# Backend address

The app must point to the correct backend host. This may be a local lab computer, shared server, or deployment environment.

When the backend address changes, update the phone app configuration and reinstall or rerun the app.

# Network security

If the system uses a local IP address or plain HTTP in a test environment, Android network security settings may need to allow that host.

# Key configuration checks

- Backend IP/domain is correct.
- Webhook path is correct.
- HTTP/HTTPS configuration is allowed.
- Phone and backend are reachable on the same network if testing locally.
- Production workflows use active webhook URLs rather than test-only URLs.

# Common environments

| Environment | Typical concern |
| --- | --- |
| Local laptop | Phone and laptop must be on the same network. |
| Lab server | Phone must reach the server address. |
| Remote server | Firewall and HTTPS settings must be correct. |

# Safe configuration process

1. Change the backend host.
2. Build and run the app.
3. Send one test request.
4. Check the backend execution history.
5. Confirm the response reaches the watch.