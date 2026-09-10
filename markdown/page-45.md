# System Architecture

Use this page when you want the full system picture: what each component does, where data flows, and where to look when something is not working.

# Big picture

```
ResearcherSideApp
      |
      | researcher actions over HTTP
      v
n8n workflows  <------>  PostgreSQL database
      ^                       ^
      |                       |
      | live data requests    | stores users, use cases,
      |                       | mappings, schedules, readings,
Android phone relay           | feedback events, and history
      ^
      | Bluetooth
      v
Wear OS smartwatch
```

# Components

- ResearcherSideApp: the dashboard researchers use to prepare and manage the study.
- Android Phone App: the relay between the smartwatch and the backend.
- Smartwatch App: the participant-facing device app that collects readings and vibrates.
- n8n: the backend workflow layer that receives requests, applies logic, and returns responses.
- PostgreSQL Database: the source of truth for users, use cases, mappings, schedules, readings, and feedback history.

# Main experiment flow

1. You configure the participant, use case, mapping, and schedule in ResearcherSideApp.
2. The smartwatch collects a reading from the participant.
3. The phone receives the reading from the watch and sends it to n8n.
4. n8n checks the active mapping for that participant and use case.
5. n8n stores the reading and feedback decision in the database.
6. n8n sends a haptic instruction back to the phone.
7. The phone sends the instruction to the smartwatch.
8. The watch vibrates.

# Researcher control flow

When you make a change in ResearcherSideApp, the dashboard sends the request to n8n. n8n updates the database. The phone and watch do not receive that change directly; they use it the next time runtime data reaches n8n.

# Important boundaries

- The smartwatch only talks to the Android phone.
- The Android phone talks to the smartwatch and n8n.
- ResearcherSideApp talks to n8n.
- n8n talks to the database.
- The database is not edited directly by the watch or phone.

# What to check first

- If researchers cannot see users, mappings, schedules, or graphs: start with ResearcherSideApp and n8n.
- If readings are missing: check the watch, phone connection, and n8n request path.
- If the watch does not vibrate: check n8n's returned haptic instruction, the phone relay, and the watch app.
- If use cases or mappings look wrong: check ResearcherSideApp, n8n mapping behavior, and the database assignment model.