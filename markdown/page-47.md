# Use Case Dictionary

# Purpose

The Use Case Dictionary defines the expected structure of research use cases and their telemetry parameters. It helps keep incoming data consistent and understandable.

# What a dictionary entry includes

| Field | Meaning |
| --- | --- |
| `dict_entry` | Automatically generated entry ID. |
| `usecase_name` | Formal name of the experiment or sensor type, such as `HeartRate` or `Pollution`. |
| `usecase_parameter_name` | Expected parameter key in the incoming data. |
| `parameter_format` | Expected data type or structure. |
| `is_required` | Whether the parameter must be present. |
| `description` | Human-readable explanation of the parameter. |

# Why this matters

The dictionary gives researchers and developers one place to define what each use case expects. This reduces confusion when adding new experiment types or changing incoming data.

# Management flow

1. A dictionary request arrives with an action and parameters.
2. The request is checked and unpacked.
3. The action router sends it to the correct operation.
4. The dictionary table is listed, added to, edited, or cleared according to the request.

# Supported actions

| Action | Description |
| --- | --- |
| `add` | Adds a parameter definition. |
| `edit` | Updates an existing parameter definition. |
| `remove_parameter` | Removes one parameter definition from a use case. |
| `remove_usecase` | Removes dictionary definitions associated with a use case. |
| `list` | Lists dictionary entries. |

# Where researchers can use the dictionary

Dictionary actions can be performed through the AI assistant. Developers can also inspect the dictionary when adding new data types or use cases.