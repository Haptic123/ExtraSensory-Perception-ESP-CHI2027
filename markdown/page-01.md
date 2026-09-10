# Adding a New Use Case

Use this page when you want to add a new sensor, context value, or experiment condition that can produce haptic feedback.

You will use three parts of the system:

- ResearcherSideApp: create the use case and define its dictionary entry.
- AI agent chat: ask for the parameters and n8n node changes you need.
- n8n Vibration Orchestrator: connect the new use-case flow to the switch using the template flow.

# Before you start

- Confirm you are working in the intended environment.
- Confirm the ResearcherSideApp can load use cases.
- Confirm you can open the `Vibration Orchestrator` workflow in n8n.
- Do not edit unrelated n8n workflows unless a maintainer asks you to.

# Step 1: Create the use case in ResearcherSideApp

Create the new use case from the ResearcherSideApp. Use a compact name with no whitespace.

Examples:

- `AirPressure`
- `UVIndex`
- `HeartRate`
- `Pollution`

The app should store the use-case ID and name after creation. This matters because the chat and n8n flows use the selected use-case context.

# Step 2: Add or review the dictionary entry

Use the [dictionary](page-47.md) feature in ResearcherSideApp to describe what this use case needs.

Include the practical details a flow needs, such as:

- What value the use case measures.
- Whether it uses watch data, phone context, an external API, or a derived value.
- Which parameters are needed.
- What value range the mapping should expect.

# Step 3: Ask the AI agent chat for implementation help

Open the AI agent chat with the new use case selected.

Ask for the n8n implementation details for the new use case. For example:

```
I created the use case AirPressure. Based on the dictionary entry, tell me what to change in the Vibration Orchestrator template flow. Focus only on the three nodes that need editing.
```

The chat should provide the values or expressions needed for the editable template nodes.

# Step 4: Update Vibration Orchestrator in n8n

Open the `Vibration Orchestrator` workflow.

Find the template flow for new use cases. Duplicate or adapt that template flow, then connect it to the switch branch for the new use case.

[REMOVED FOR ANONYMITY]

Only change the three required nodes in the template flow. Use the values provided by the AI agent chat.

Do not change unrelated branches unless you are intentionally maintaining the workflow.

# Step 5: Test the new use case

After saving the workflow:

- Send or simulate one request for the new use case.
- Confirm n8n follows the new switch branch.
- Confirm the flow produces the expected value.
- Confirm the mapping decision is stored or returned as expected.
- Confirm the ResearcherSideApp can show the use case and relevant mapping state.

# What to check if it does not work

- The use-case name in ResearcherSideApp, dictionary, and n8n switch must match.
- The selected use-case ID should be available before sending chat requests.
- The new branch should be connected to the Vibration Orchestrator switch.
- The three edited template nodes should match the AI agent chat instructions.
- The mapping for the new use case should exist and be assigned where needed.