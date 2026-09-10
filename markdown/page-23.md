# n8n Workflows Breakdown

> 💼 **Purpose of this page**
> 
> 
> This page explains how the n8n workflows in the Smartwatch Haptic Feedback System are divided, how they communicate, which components call them, and which workflows should be edited for different types of changes.
> 
> It is intended as a system-maintenance map. For node-level explanations, installation instructions, or testing procedures, use the linked documentation pages.
> 

---

# Workflow architecture

The n8n backend is divided into three layers:

1. **Public entrypoint workflows**Receive requests from the Android phone or ResearcherSideApp.
2. **Internal manager workflows**Perform focused database actions such as managing mappings, schedules, and dictionary entries.
3. **AI analysis workflows**Answer researcher questions using project documentation, literature, participant data, and mapping information.

---

# Workflow groups

## Public entrypoints

These workflows expose production webhooks and must be active for the complete system to operate:

- `Vibration Orchestrator`
- `DB Manager`
- `Chat Orchestrator`

## Internal manager workflows

These workflows are normally called by another workflow through an **Execute Workflow** node:

- `Mapping Manager`
- `Schedule Manager`
- `Dictionary Manager`
- `Use Case Builder`

They should not normally be called directly by the Android applications.

## AI workflows

The current read-only AI analysis system consists of:

- `Expert Panel Agent`
- `Agent Expert - Project Context`
- `Agent Expert - Literature`
- `Agent Expert - Participant Data`
- `Agent Expert - Mapping Design`

## Older workflow

- `Knowledge Agent`

The current `Chat Orchestrator` routes read-only questions to `Expert Panel Agent`, not to a separate Knowledge Agent. Treat `Knowledge Agent` as an older standalone implementation.

---

# Quick workflow reference

| Workflow | Primary responsibility | Called by | Main data source | Change risk |
| --- | --- | --- | --- | --- |
| Vibration Orchestrator | Live sensor processing and haptic decisions | Android phone | PostgreSQL and external APIs | High |
| DB Manager | ResearcherSide dashboard and database endpoints | ResearcherSide and phone | PostgreSQL | High |
| Chat Orchestrator | Chat validation, context, planning, and routing | ResearcherSide AI chat | PostgreSQL and subworkflows | High |
| Mapping Manager | Mapping creation, assignment, editing, and history-sensitive actions | Chat Orchestrator | Mapping tables and sensor history | Very high |
| Schedule Manager | Schedule creation and state management | Chat Orchestrator | `user_schedules` | Medium |
| Dictionary Manager | Use-case parameter dictionary operations | Chat Orchestrator | `UseCaseDictionary` and `api_pool` | Medium |
| Use Case Builder | Generates implementation instructions for a new API use case | Chat Orchestrator | Dictionary and API metadata | Medium |
| Expert Panel Agent | Coordinates grounded read-only analysis | Chat Orchestrator | Four expert tools | Medium |
| Project Context Expert | Explains project architecture and implementation | Expert Panel | Project documentation | Low |
| Literature Expert | Retrieves academic evidence | Expert Panel | Literature vector store | Low |
| Participant Data Expert | Analyzes participants, readings, assignments, and feedback | Expert Panel | PostgreSQL | Medium |
| Mapping Design Expert | Explains mappings or generates advisory proposals | Expert Panel | PostgreSQL and design context | Medium |
| Knowledge Agent | Simplified standalone knowledge answer flow | Legacy/manual invocation | PostgreSQL and OpenAI | Low |

---

# 1. Vibration Orchestrator

## Purpose

Processes live sensor or external API data and converts it into smartwatch haptic feedback.

## Main entrypoint and responsibilities

```
POST /webhook/usecase-routing
```

Main responsibilities:

- Receive data from the Android phone.
- Identify the requested use case.
- Use the supplied sensor value or retrieve a value from an external API.
- Find the participant’s active feedback mapping.
- Calculate pulses, intensity, duration, and interval.
- Store the reading and feedback decision.
- Return the haptic command to the phone.

## Main data flow

```
Watch sensor
→ Android phone
→ Vibration Orchestrator
→ Use-case branch
→ Sensor value or external API
→ Active mapping
→ Haptic calculation
→ Database storage
→ Android phone
→ Watch vibration
```

## Credentials needed

- PostgreSQL
- External API credentials, where required

## What researchers may edit

Researchers should normally edit this workflow only when adding a new use case.

Safe edit areas:

- Add a new condition to `Route By Sensor Type`.
- Copy and connect the existing use-case template branch.
- Change the use-case name.
- Configure the API request.
- Configure the numeric response-value extraction.
- Adjust the branch rate limit when required.

Researchers should not edit:

- Shared mapping-resolution logic
- Database insertion logic
- Generic response nodes
- Existing unrelated use-case branches

---

# 2. DB Manager

## Purpose

Provides the backend endpoints used by ResearcherSideApp and several Android phone configuration checks.

## Main responsibilities

- Retrieve participants and devices.
- Retrieve mappings and current assignments.
- Retrieve mapping history.
- Manage monitoring state.
- Retrieve sensor readings and feedback events.
- Provide available sensor and use-case information.
- Handle stopped-monitoring alerts.
- Support ResearcherSide dashboard operations.

Example endpoints include:

```
GET /webhook/get-users
GET /webhook/current-configurations
GET /webhook/sensor-data
GET /webhook/get-sensor-types
GET /webhook/monitoring-config
GET /webhook/users-mappings-history
POST /webhook/stopped-monitoring-alert
```

## Main data flows

```
ResearcherSide or Android phone
→ DB Manager webhook
→ Request validation
→ PostgreSQL query or update
→ Response formatting
→ Calling application
```

## Credentials needed

- PostgreSQL
- SMTP, for stopped-monitoring email alerts

## What researchers may edit

Researchers should normally not edit DB Manager.

A maintainer may edit it when:

- ResearcherSide requires a new endpoint.
- A new database field must be returned.
- Monitoring or alert behavior changes.
- A dashboard query or response structure is incorrect.
- Updating the `Send Offline Email` target email address

Be careful when changing response field names because ResearcherSide depends on the exact JSON structure.

---

# 3. Chat Orchestrator

## Purpose

Receives ResearcherSide AI-chat requests, loads the current application context, and routes each request to the correct specialized workflow.

## Main entrypoint and responsibilities

```
POST /webhook/chat
```

Main responsibilities:

- Validate the chat payload.
- Load the selected participant, use case, and mapping context.
- Maintain the chat session.
- Identify the researcher’s intent.
- Route the request to one workflow.
- Return the final structured response to ResearcherSide.

Possible targets:

- Mapping Manager
- Schedule Manager
- Dictionary Manager
- Use Case Builder
- Expert Panel Agent
- Clarification response

## Main data flow

```
ResearcherSide chat
→ Chat Orchestrator
→ Validate input
→ Load session and context
→ Planner
→ Selected subworkflow
→ Structured response
→ ResearcherSide
```

## Credentials needed

- PostgreSQL
- OpenAI

## What researchers may edit

Researchers should not normally edit this workflow.

Maintainers may edit:

- Planner instructions (prompt)
- Routing rules
- Application-context fields
- Supported target workflows
- Final response formatting

Changes here can affect every AI feature, so test all major chat intents after editing.

---

# 4. Mapping Manager

## Purpose

Performs deterministic mapping operations requested through the AI assistant.

## Main responsibilities

Supported operations include:

- List active mappings
- List all mappings
- Add a mapping
- Change a mapping
- Assign a mapping
- Duplicate a mapping for one participant
- Remove or deactivate a mapping
- Brainstorm new mapping ideas

## Main data flow

```
Chat Orchestrator
→ Mapping Manager
→ Action router
→ Validation
→ PostgreSQL query or update
→ Formatted response
→ Chat Orchestrator
```

## Credentials needed

- PostgreSQL
- OpenAI, for mapping brainstorming

## What researchers may edit

Researchers should not edit this workflow directly.

Maintainers may edit it when changing:

- Mapping actions
- Mapping validation rules
- Shared versus participant-specific behavior
- Assignment logic
- Deactivation and reassignment behavior
- Mapping brainstorm context

This is a high-risk workflow. Always test:

- Shared mapping edits
- Participant-specific copies
- Assignment history
- Mapping deactivation
- Participant reassignment

---

# 5. Schedule Manager

## Purpose

Manages participant schedules requested through the AI assistant.

## Main responsibilities

- Add, change, activate and decativate a schedule
- List active schedules
- List all schedules

Main schedule fields include:

- Participant
- Interval
- Next run date
- Measure type
- Trigger percentage
- Active state

## Main data flow

```
Chat Orchestrator
→ Schedule Manager
→ Parse schedule parameters
→ Action router
→ PostgreSQL query or update
→ Formatted response
```

## Credentials needed

- PostgreSQL

## What researchers may edit

Researchers should manage schedules through ResearcherSide or the AI assistant rather than editing this workflow.

Maintainers may edit:

- Supported schedule actions
- Validation requirements
- Date calculations
- Active/inactive behavior
- Use-case filtering

---

# 6. Dictionary Manager

## Purpose

Manages the Yellow Book use-case dictionary.

## Main responsibilities

- List dictionary entries
- Retrieve, add, edit and remove one use case’s parameters
- Remove all dictionary entries for a use case

The dictionary defines:

- Parameter name
- Parameter format
- Whether it is required
- Description
- Fixed value, when applicable
- Related external API

## Main data flow

```
Chat Orchestrator
→ Dictionary Manager
→ Action router
→ UseCaseDictionary and api_pool
→ Formatted response
```

## Credentials needed

- PostgreSQL

## What researchers may edit

Researchers should usually manage dictionary entries through ResearcherSide or the AI assistant.

Maintainers may edit:

- Supported dictionary actions
- Parameter validation
- API-pool relationships
- Returned dictionary structure

Keep the use-case name identical across the database, Vibration Orchestrator, ResearcherSide, and device applications.

---

# 7. Use Case Builder

## Purpose

Generates copy-paste-ready instructions for adding a new external API-based use case to the Vibration Orchestrator.

## Main responsibilities

- Load the selected use case’s dictionary parameters.
- Load matching API metadata.
- Identify the API endpoint.
- Identify the numeric response path.
- Generate the required template changes.
- Explain where each generated value should be pasted.

The builder does not edit or activate the workflow automatically.

## Main data flow

```
Chat Orchestrator
→ Use Case Builder
→ Dictionary and API metadata
→ Validate required information
→ Generate template instructions
→ Researcher response
```

## Credentials needed

- PostgreSQL
- OpenAI

## What researchers may edit

Researchers normally do not edit the Use Case Builder itself.

They use its output to edit only the marked template areas inside Vibration Orchestrator:

- `Set type`
- `Construct API Request`
- `Extract`
- `Route By Sensor Type`
- Optional rate limit

Maintainers may edit the builder when the Vibration Orchestrator template or generated output format changes.

## Related pages

- [Adding a New Use Case](page-01.md)

---

# 8. Expert Panel Agent

## Purpose

Coordinates read-only analysis by selecting the relevant expert workflows.

## Main responsibilities

- Answer project and architecture questions.
- Retrieve academic evidence.
- Analyze participant and experiment data.
- Explain existing mappings.
- Generate advisory mapping proposals when explicitly requested.
- Return citations, warnings, findings, and recommendations in a structured format.

It must never perform database mutations.

## Main data flow

```
Chat Orchestrator
→ Expert Panel Agent
→ Selected expert tools
→ Combined grounded response
→ Chat Orchestrator
```

## Credentials needed

- OpenAI
- Credentials required by the connected expert workflows

## What researchers may edit

Researchers should not edit this workflow.

Maintainers may edit:

- Expert-selection rules
- Read-only boundaries
- Response schema
- Citation handling
- Proposal-generation rules
- Experiment-summary behavior

Changing the response schema requires checking ResearcherSide compatibility.

## Related pages

- AI Assistant and Dictionary [LINK REMOVED FOR ANONYMITY]

---

# 9. Agent Expert – Project Context

## Purpose

Answers technical questions about the project and system architecture.

## Main responsibilities

- Explain component responsibilities.
- Explain n8n, PostgreSQL, Android, watch, and ResearcherSide integration.
- Explain workflow ownership.
- Explain supported system behavior.

## Credentials needed

- OpenAI
- Project-context data source or vector store

## What researchers may edit

Researchers should not edit the workflow.

Maintainers may update:

- Project documentation sources
- System instructions
- Architecture context
- Outdated technical facts

---

# 10. Agent Expert – Literature

## Purpose

Retrieves and explains academic literature relevant to haptic feedback and sensory substitution.

## Main responsibilities

- Retrieve relevant papers.
- Explain academic concepts.
- Return source information and citations.
- Distinguish a single retrieved study from broader evidence.

## Credentials needed

- OpenAI
- Literature vector store or retrieval source

## What researchers may edit

Researchers should not edit the workflow.

Maintainers may update:

- Literature files
- Vector-store connection
- Retrieval instructions
- Citation-output format

---

# 11. Agent Expert – Participant Data

## Purpose

Analyzes participant, sensor, assignment, and feedback data.

## Main responsibilities

- Summarize participant readings.
- Analyze a use-case cohort.
- Review sensor-data coverage.
- Review active mappings and assignment history.
- Review feedback or alert activity.
- Identify missing or insufficient data.

## Main data flow

```
Expert Panel
→ Participant Data Expert
→ PostgreSQL queries
→ Findings and evidence
→ Expert Panel
```

## Credentials needed

- PostgreSQL
- OpenAI, when used for interpretation

## What researchers may edit

Researchers should not edit this workflow.

Maintainers may edit:

- Analysis queries
- Supported scopes
- Evidence references
- Findings structure
- Data-quality warnings

Avoid making claims stronger than the available records.

---

# 12. Agent Expert – Mapping Design

## Purpose

Explains current mappings and generates advisory mapping proposals when requested.

## Main responsibilities

Two modes are supported:

### Existing-mapping analysis

- Explain current mapping ranges.
- Compare haptic parameters.
- Describe assignment information.
- Discuss likely feedback differences.

### Proposal design

- Brainstorm new mapping options.
- Suggest gentler or stronger feedback.
- Suggest participant-specific alternatives.
- Generate advisory parameter proposals.

Proposals are not automatically saved.

## Credentials needed

- PostgreSQL
- OpenAI

## What researchers may edit

Researchers should not edit the workflow directly.

Maintainers may edit:

- Existing-mapping analysis rules
- Proposal requirements
- Haptic parameter constraints
- Output structure
- Safety and feedback-burden instructions

## Related pages

- Mapping sections in [ResearcherSideApp Documentation](page-34.md)

---

# 13. Knowledge Agent

## Purpose

**[DEPRECATED]** Provides a simpler knowledge-answer flow using the selected use case and its active mappings.

## Main responsibilities

- Fetch active mappings for a use case.
- Add them to the AI context.
- Answer the researcher’s question.
- Return a text response.

## Main data flow

```
Manual or legacy workflow call
→ Fetch active mappings
→ OpenAI
→ Text response
```

## Credentials needed

- PostgreSQL
- OpenAI

## What researchers may edit

Researchers should not edit this workflow.

The current Chat Orchestrator uses the Expert Panel for read-only analysis. Keep this workflow only for legacy or standalone use unless the routing architecture is intentionally changed.

---

# Workflow dependency map

```
ResearcherSideApp
├── DB Manager
└── Chat Orchestrator
    ├── Mapping Manager
    ├── Schedule Manager
    ├── Dictionary Manager
    ├── Use Case Builder
    └── Expert Panel Agent
        ├── Project Context Expert
        ├── Literature Expert
        ├── Participant Data Expert
        └── Mapping Design Expert
```

---

# Important import note

After importing the workflows into a new n8n instance, re-select the target workflow inside every:

- Execute Workflow node
- AI workflow tool node

Exported workflow IDs may not match the IDs assigned in the new n8n environment.

---

# Related documentation

- [Getting Started with n8n](page-21.md)
- [n8n Node Types Used in the System](page-22.md)
- [Running and Testing Workflows](page-25.md)
- n8n Developer Reference [LINK REMOVED FOR ANONYMITY]
- [Setting Credentials on n8n](page-37.md)
- Smartwatch Haptic Workflow Repository [LINK REMOVED FOR ANONYMITY]