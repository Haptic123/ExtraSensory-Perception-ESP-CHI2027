# Vibration Orchestrator for Researchers

Use this page when you need to modify the n8n Vibration Orchestrator workflow for a new use case.

# What researchers should edit

Researchers should usually only touch the `Vibration Orchestrator` workflow.

The practical task is to connect a new use-case flow to the workflow switch. The workflow should already include a template flow for new use cases.

# What changes

For a new use case, the expected change is small:

- Use the existing template flow.
- Connect it to the switch branch for the new use case.
- Change only the three required nodes in that template flow.

The AI assistant chat in ResearcherSideApp can help provide the values or expressions for those three nodes.

# What not to change

- Do not edit unrelated branches.
- Do not edit DB Manager unless a maintainer asks you to.
- Do not edit Mapping Manager unless a maintainer asks you to.
- Do not change active participant workflows during a live session unless the study lead approves it.

# Where to find the full steps

Use the top-level `Adding a New Use Case` page for the complete process.