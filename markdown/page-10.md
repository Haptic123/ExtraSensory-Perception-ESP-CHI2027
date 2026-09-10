# Communication Between Components

Use this page when you want to understand how the system parts talk to each other.

# Big picture

```
ResearcherSideApp
      |
      | HTTP webhook calls
      v
n8n workflows  <------>  PostgreSQL database
      ^                       ^
      |                       |
      | HTTP POST/GET         | stores users, use cases,
      |                       | mappings, schedules, readings,
Android phone relay           | feedback events, and context
      ^
      | Bluetooth SPP
      v
Wear OS smartwatch
```

# What each connection means

- ResearcherSideApp -> n8n: The dashboard sends researcher actions to n8n. Examples include loading users, creating use cases, assigning mappings, editing schedules, and asking the assistant for help.
- n8n -> PostgreSQL: n8n reads and writes the system data. PostgreSQL is the source of truth for users, use cases, mappings, assignments, schedules, readings, and feedback events.
- Android phone -> n8n: The phone sends live sensor and context payloads to n8n and receives haptic instructions in response.
- Smartwatch <-> Android phone: The watch and phone communicate over Bluetooth. The watch sends readings to the phone, and the phone sends vibration commands back to the watch.

# Important boundaries

- The smartwatch does not talk directly to n8n, PostgreSQL, or the ResearcherSideApp.
- The Android app does not write directly to the database.
- The ResearcherSideApp does not directly trigger watch vibration. It changes configuration, and runtime flows use that configuration.
- n8n is the backend layer that connects app requests to database operations and haptic decisions.

# Main runtime flow

This flow applies to the `HeartRate` use case and to future use cases that rely on body-sensor data from the smartwatch.

1. The smartwatch reads a body-sensor value, such as heart rate.
2. The watch sends the reading to the Android phone.
3. The phone adds identifiers and context, then sends the request to n8n.
4. n8n resolves the user's active mapping through `User_UC_Mappings -> feedback_config_rules -> UseCase`.
5. n8n applies the mapping, stores the reading and feedback decision, and returns a haptic command.
6. The phone relays the command to the watch.
7. The watch vibrates.

For other use cases that do not rely on smartwatch body sensors, the Android phone sends the user's location data directly to n8n. n8n then uses that location data, and any relevant external or derived context, to decide what haptic command should be returned.

# Researcher configuration flow

1. You make a change in the ResearcherSideApp.
2. The app sends an HTTP request to n8n.
3. n8n validates the request and updates PostgreSQL.
4. Runtime flows use the updated configuration the next time data arrives.