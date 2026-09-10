# Safe Database Changes

# Purpose

This page explains how to make database changes safely without disrupting an active study.

# Before changing anything

- Confirm which database you are connected to.
- Create a backup.
- Avoid direct edits during a live participant session.
- Prefer adding or deactivating rows over deleting them.
- Test with one known user before using the change in a study.

# Changing haptic rules

Recommended process:

1. List current active rules.
2. Add the new rule as inactive or test it with a non-live participant.
3. Activate the rule only when verified.
4. Keep old rules inactive when possible for traceability.
5. Confirm generated alerts reference the expected rule.

# Changing schedules

Check these fields carefully:

- `user_id`
- `interval_days`
- `next_run_date`
- `measure_type`
- `trigger_percentage`
- `active`

# Changing dictionary entries

Only update dictionary definitions when the apps and workflows that send data are aligned with the new expected parameters.

# Common mistakes

| Mistake | Result |
| --- | --- |
| Updating the wrong database | Dashboard and n8n show inconsistent data. |
| Deleting rules | Harder to reconstruct what happened in a study. |
| Changing a use-case name | Existing mappings or data may stop matching. |
| Editing during a live session | Participant feedback may change unexpectedly. |