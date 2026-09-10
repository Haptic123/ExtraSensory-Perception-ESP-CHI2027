# Mappings and Haptic Feedback

Use this page to understand how haptic feedback mappings work in the ResearcherSideApp.

# What a mapping is

A mapping tells the system how to turn a measured value into a vibration pattern.

For example, a heart-rate mapping might say that one value range should create a soft vibration and another value range should create a stronger or longer vibration.

Mappings can include settings such as:

- Value range
- Number of pulses
- Intensity
- Duration
- Interval between pulses

# Shared mappings

A mapping can be shared by more than one participant. This is useful when multiple participants should receive the same haptic behavior.

Be careful when editing a shared mapping. A global edit can affect every participant assigned to that mapping.

# Editing for one participant

If a change should apply only to one selected participant, use the selected-user-only mapping flow. The system creates a copy of the mapping and assigns that copy to the selected participant. This avoids accidentally changing the mapping for everyone else.

# Mapping history

The system keeps mapping assignment history. This helps you understand which mapping was active for a participant over time.