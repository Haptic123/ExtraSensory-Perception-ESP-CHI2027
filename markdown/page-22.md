# n8n Node Types Used in the System

# Purpose

This page explains the main n8n node types used in the system in plain language.

# Webhook

Creates an HTTP endpoint. Apps and dashboards call these endpoints to send data or request information.

# Respond to Webhook

Returns the final response to the app or dashboard. Without this node, the caller may wait without receiving a clear result.

# PostgreSQL

Runs database queries. Used for users, mappings, schedules, dictionary entries, sensor data, and assistant context.

# Code

Runs small JavaScript transformations. Used for validation, parsing, date calculation, response formatting, and routing preparation.

# Switch

Routes a request based on an action or type. Common action examples include `add`, `list`, `change`, `activate`, and `deactivate`.

# Merge

Combines branches back into one response path.

# Set

Creates or updates fields used later in the workflow.

# AI model and LLM chain nodes

Used by the assistant workflows to classify requests, answer questions, and route structured actions.

# Practical reading tip

When inspecting a workflow, follow the data from left to right. Start at the trigger, then inspect parsing, database access, routing, and final response.