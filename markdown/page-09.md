# Chat and Knowledge Assistant

# What the assistant is

The assistant is a chat interface for asking questions about the selected study context and for requesting supported system actions. The chat appears in the ResearcherSideApp, while n8n receives each message, decides which workflow should handle it, and returns the answer.

The assistant can use the currently selected use case, participant, mapping, all-users scope, recent messages, database records, project documentation, and academic sources. This means the answer can change when you select a different participant or use case.

# Before you send a message

1. Select the correct use case.
2. Select a participant, or choose **All Users** for an experiment-level question.
3. Check the Context Drawer if you want to confirm what the assistant can currently see.
4. Use a new chat session when you want to start a separate topic.

A participant must belong to the selected use case before participant-specific chat can continue.

# What the assistant can do

## Questions and read-only analysis

The assistant can:

- Explain the project, its components, database rules, and n8n workflows.
- Explain haptic-feedback terms, mapping parameters, and current configurations.
- Answer academic questions using uploaded literature and return source information.
- Summarize a selected participant or the complete selected use case.
- Analyze sensor coverage, recorded values, feedback activity, mapping assignments, assignment history, and data limitations.
- Compare current mappings.
- Suggest up to three mapping options with parameters, reasoning, trade-offs, warnings, and evidence references.
- Generate step-by-step guidance for adding an external API-based use case.

Knowledge answers, analyses, and mapping proposals are read-only. A proposal shown in the chat is not saved, activated, or assigned.

## Supported system actions

When the request is clear and complete, the assistant can route these actions to deterministic n8n workflows:

- **Mappings:** list active or all mappings; add or remove a mapping; change a global mapping; duplicate and change a mapping for one participant; assign an existing mapping.
- **Dictionary:** list or retrieve entries; add, edit, or remove a parameter; remove a use case's dictionary entries.
- **Schedules:** list active or all schedules; add or change a schedule; activate or deactivate a schedule.
- **Use-case setup:** generate implementation instructions for the Vibration Orchestrator template. This produces guidance only and does not edit the workflow automatically.

The current release supports one active mapping per participant globally. It does not maintain a separate active mapping for every participant-and-use-case combination.

# How it works in n8n

```
ResearcherSideApp
    |
    | POST /webhook/chat
    v
Chat Orchestrator
    |
    +-- Mapping Manager
    +-- Expert Panel Agent
    +-- Dictionary Manager
    +-- Schedule Manager
    +-- Use Case Builder
    +-- Clarification response
    |
    v
Reply returned to the app and session history updated
```

## Chat Orchestrator

The **Chat Orchestrator** is the entry point for every chat message.

1. The ResearcherSideApp sends the message with a session ID, use-case ID, use-case name, selected participant details when available, the analysis scope, recent history, and other visible context.
2. The workflow validates that the required message, session, and use-case information is present.
3. It creates or updates the session in the PostgreSQL `agent_session` table.
4. It loads the latest conversation and active mapping context from the `v_agent_context` database view.
5. GPT-4o acts as a planner. It classifies the request as mapping, knowledge, dictionary, scheduling, use-case building, or clarification and returns a structured routing decision.
6. n8n checks the model's decision and sends the request to exactly one supported workflow.
7. The selected workflow validates its inputs, reads or updates the database when allowed, or calls the relevant expert.
8. The result is formatted for the ResearcherSideApp. The app can show the reply together with proposal, warning, and source cards.
9. n8n saves the user message and assistant reply to the session history.

The model plans and routes the request. Database changes are performed by fixed workflow steps and parameterized database queries, not by the model directly.

## Expert Panel Agent

All knowledge, explanation, analysis, research, and recommendation requests go to the read-only **Expert Panel Agent**. GPT-4o selects only the expert or experts needed for the question.

The connected experts are:

- **Agent Expert - Project Context:** searches the uploaded project documentation. Use it for system architecture, component responsibilities, database contracts, the JavaFX application, Android and smartwatch apps, and n8n implementation questions.
- **Agent Expert - Literature:** searches uploaded academic sources. Use it for research evidence about haptic feedback, tactons, sensory substitution, interoception, wearable feedback, urgency, vibration timing, feedback burden, and related concepts.
- **Agent Expert - Participant Data:** reads PostgreSQL records for either one selected participant or the full selected use case. It summarizes readings, coverage, values, feedback activity, mapping assignments, and data-quality limits.
- **Agent Expert - Mapping Design:** reads current mappings, the selected participant's assignment, and recent sensor statistics. It can explain current mappings or generate read-only mapping proposals when the user explicitly asks for ideas, personalization, or design changes.

The Expert Panel combines the relevant results into one concise answer. It keeps returned database references and file citations, separates current mappings from proposals, and does not perform changes.

# AI model

The current active implementation uses **OpenAI GPT-4o** in the Chat Orchestrator, Expert Panel Agent, Participant Data Expert, Mapping Design Expert, project and literature retrieval, mapping brainstorming, and use-case guidance.

Changing the configured model in n8n changes this implementation detail, so this page should be reviewed whenever the workflow model settings change.

# OpenAI vector stores

Two vector stores in the OpenAI platform provide searchable knowledge to the assistant.

## Project documentation vector store

Contains five project documents covering the agent implementation, system context, retrieval configuration, knowledge base, and user stories. The Project Context Expert must search this store and retrieves up to five relevant results.

smartwatch-haptic-project-dev_vs_6a2d3128f3908191bfcabb99e9c73fce.zip [LINK REMOVED FOR ANONYMITY]

## Academic literature vector store

Contains seven academic papers about haptic feedback and related research topics. The Literature Expert must search this store, retrieves up to eight relevant results, and reports file citations when available.

smartwatch-haptic-literature-dev_vs_6a2d3137c91c8191bdd89eadb64e9d36.zip [LINK REMOVED FOR ANONYMITY]

Both vector stores were in a completed state in the 18 July 2026 export.

The Participant Data Expert and Mapping Design Expert do not use these vector stores for live experiment facts. They use the PostgreSQL database so their analysis reflects current participants, readings, mappings, and assignments.

# Context awareness

The assistant receives context automatically from the ResearcherSideApp. This includes:

- The selected use case and its ID.
- The selected participant, participant name, assignment, and mapping ID when available.
- Whether **All Users** is selected.
- Whether the request should be participant-level or use-case-level.
- Active mapping information loaded by n8n.
- Recent messages and a short summary of the latest structured answer.

Context lets users ask follow-up questions such as “What does that mapping mean?” or “Who is the assigned participant?” without repeating every detail. If a follow-up could refer to more than one mapping or participant, the assistant should ask which one you mean instead of guessing.

Changing the selected participant or use case changes the context sent with the next message.

# Session history

Chat history is available at two levels:

- **In the ResearcherSideApp:** each use case can have multiple named chat sessions. Users can start a new session, reopen previous sessions, browse eight sessions per history page, and delete a locally saved session. The app stores these sessions and their displayed messages on the researcher's computer.
- **In PostgreSQL:** n8n stores the conversation in `agent_session.conversation_history`. The database retains the latest 24 messages for each session, which is normally 12 user-and-assistant exchanges.
- **For each new request:** the app also sends up to 12 recent messages, shortened when necessary, plus a summary of the latest structured response. This supports follow-up questions within the same session.

Deleting a chat session in the current ResearcherSideApp removes the local saved session after a confirmation dialog. The current implementation does not send a request to delete the corresponding `agent_session` record from PostgreSQL.

# Suggested prompts and shortcuts

When the chat is empty, the app shows suggested prompt cards. Typing `$` also opens command suggestions.

- `$mapping` — show the current feedback mappings.
- `$knowledge` — explain the background of the selected experiment.
- `$dictionary` — show use cases in the dictionary.
- `$schedule` — show active schedules.
- `$summarize` — summarize the selected participant or selected experiment scope.

You can also write normal sentences:

```
Explain mapping ID 140 in simple language.
```

```
Summarize this experiment for all selected users.
```

```
What does the literature say about feedback burden?
```

```
Suggest a gentler mapping for the selected participant based on recent readings. Do not change anything.
```

```
List the active schedules for this participant.
```

# Approval before actions

The read-only Expert Panel never saves a proposal or changes a record.

For mapping, dictionary, or schedule changes, the current release uses the following approval rule:

- A clear and complete action request from the user is treated as approval to perform that action.
- The assistant validates required IDs and values before routing the action.
- If the target, scope, or required information is unclear, the assistant asks a clarification question and does not perform the change.
- A participant-only mapping change is separated from a global mapping change. If a shared mapping could be affected and the scope is unclear, the assistant asks whether the change should be global or participant-only.
- The chat currently has no separate **Approve** button and no second confirmation prompt after a complete action request. A supported change may run immediately after the message is sent.

For safer use, first ask the assistant to list the current record and IDs. Then send one exact action with the intended scope. Do not request changes during a live participant session unless the study procedure allows it.

# Example interaction

**Starting context:** HeartRate is selected and participant 333 is selected.

**Researcher:**

`$summarize`

**Assistant:**

Returns a read-only summary of participant 333's recent readings, feedback activity, current mapping assignment, and data limitations.

**Researcher:**

`Suggest a gentler mapping based on this participant's recent readings. Do not change anything.`

**Assistant:**

Calls the Participant Data and Mapping Design experts as needed, then shows one or more proposal cards with parameters, reasoning, trade-offs, warnings, and evidence. Nothing is saved or assigned.

**Researcher:**

`Assign existing mapping ID 191 to participant 333.`

**Assistant:**

Treats this exact instruction as approval, routes it to Mapping Manager, validates both IDs, performs the assignment if valid, and returns the result. There is no separate approval screen.

# Important limits

- The assistant can be wrong or may lack enough evidence. Check warnings and sources.
- Academic answers are limited to the papers stored in the literature vector store.
- Project answers are limited to the uploaded project documents.
- A missing database record means the assistant lacks evidence; it does not prove that an event never happened.
- Mapping proposals are research guidance, not medical advice and not automatically applied.
- Use Case Builder produces copy-and-paste instructions. A maintainer must still review and apply them in n8n.
- The assistant should never invent participant, mapping, schedule, or use-case IDs.

# Related documentation

- [ResearcherSideApp](page-34.md)
- [n8n](page-27.md)
- n8n Developer Reference [LINK REMOVED FOR ANONYMITY]
- [Communication Between Components](page-10.md)