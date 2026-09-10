# Getting Started with n8n

n8n is the workflow-automation platform used as the backend layer of the Smartwatch Haptic Feedback System.

It receives requests from the system applications, communicates with the database and external services, processes data, and returns responses to the calling application.

This page provides a basic orientation for people who are unfamiliar with n8n. It does not explain the system’s individual workflows in detail.

---

# Opening n8n

Open the n8n editor using the address configured for the server, the default address is usually:

```
[LINK REMOVED FOR ANONYMITY]
```

Sign in using the n8n administrator account.

After signing in, the main workflow list should appear.

> If n8n does not open, confirm that the n8n service is running before troubleshooting individual workflows.
> 

---

# What is a workflow?

A workflow is a visual sequence of connected nodes.

Each node performs one task, such as:

- Receiving an HTTP request
- Validating or transforming data
- Querying PostgreSQL
- Calling an external API
- Running another workflow
- Using an AI model
- Returning a response

Data moves between nodes from left to right along the connections.

---

# Main parts of the n8n editor

## Nodes

Each node performs a specific operation.

Selecting a node opens its configuration panel, where you can inspect:

- Input fields
- Parameters
- Expressions
- Credentials
- Output data
- Errors

## Executions

The Executions view shows previous workflow runs.

Use it to inspect:

- Whether a workflow succeeded or failed
- Which node failed
- The input and output of each node
- Error messages
- Execution time

## Test and production webhooks

Webhook nodes normally provide two URLs:

```
/webhook-test/...
```

Used while manually testing a workflow in the n8n editor.

```
/webhook/...
```

Used by the installed applications when the workflow is active.

> The Android application and ResearcherSideApp should normally use the production `/webhook` URL.
> 
> 
> ```
> /webhook
> ```
> 

---

# Running a workflow manually

To test a workflow:

1. Open the workflow.
2. Select **Execute Workflow** or **Listen for Test Event**, depending on its trigger.
3. Send the test request.
4. Follow the highlighted execution path.
5. Select each relevant node to inspect its input and output.
6. Confirm that the final response is correct.

A manual test does not always prove that the production webhook works. After testing in the editor, also test the active workflow through its production URL.

---

# Understanding node data

Each node receives items containing JSON data.

A simplified item may look like:

```json
{
  "userId": 1,
  "type": "HeartRate",
  "value": 82
}
```

Select the **Input** and **Output** tabs inside a node to see how the data changes as it moves through the workflow.

When debugging, begin at the first node and follow the execution one node at a time until the data becomes incorrect or a node fails.

---

# Expressions

n8n expressions allow one node to use data produced by another node.

Expressions commonly appear in this form:

```
{{ $json.value }}
```

This reads the `value` field from the current item.

An expression may also reference a named node:

```
{{ $('Node Name').first().json.value }}
```

Before changing an expression:

- Confirm the referenced node name.
- Confirm that the required field exists.
- Inspect the node’s actual output.
- Preserve the expected data type.

---

# Credentials

Credentials store access information for services such as:

- PostgreSQL
- OpenAI
- Email
- External APIs

Credentials should be configured through n8n’s credential manager rather than written directly inside nodes.

Never place passwords, API keys, or private tokens in:

- Sticky notes
- Code nodes
- Exported workflow files
- Screenshots
- Public documentation

[For credential setup, open the Setting Credentials on n8n page.](page-36.md)

---

# Activating workflows

A webhook workflow must normally be active before another application can call its production URL.

After changing a workflow:

1. Save it.
2. Activate it if it is a public entrypoint.
3. Confirm that its production webhook is registered.
4. Test it from the application that normally calls it.

Internal workflows may be triggered through **Execute Workflow** nodes rather than public webhooks.

---

# Important rule after importing workflows

Workflow references may not survive a clean import correctly.

After importing the system workflows, inspect every:

- **Execute Workflow** node
- AI workflow-tool node

Re-select the intended target workflow from the dropdown and save the workflow.

A node may show an old workflow name while still containing an invalid internal workflow ID.

---

# Safe editing rules

Before changing a workflow:

1. Export or duplicate the current working version.
2. Use test participants and test data.
3. Change one logical area at a time.
4. Run the affected branch manually.
5. Inspect the database and final response.
6. Test the real calling application.
7. Keep the previous export until the new version is validated.

Researchers should only edit workflow areas explicitly identified as researcher-editable in the documentation.

Do not modify shared database logic, participant-assignment behavior, or application response structures without understanding the dependent components.

---

# Where to continue

Use the following pages according to your task:

- **[n8n Workflows Breakdown](page-23.md)** — understand the purpose and ownership of each workflow.
- **[Running and Testing Workflows](page-25.md)** — test webhooks and inspect executions.
- **[n8n Node Types Used in the System](page-22.md)** — understand the node types used by the project.
- [**Setting Credentials on n8n**](page-37.md) — configure PostgreSQL, OpenAI, email, and other credentials.
- [**Vibration Orchestrator for Researchers**](page-21.md) — safely connect a new use-case branch.
- **[Adding a New Use Case](page-01.md)** — follow the complete use-case creation process.
- **n8n Developer Reference** [LINK REMOVED FOR ANONYMITY] — maintain mapping, schedule, AI, and database behavior.


💡

> Start with the workflow breakdown before editing any workflow.
> 
