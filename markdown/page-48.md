# Smartwatch Haptic Feedback Hub


💡 Welcome. This documentation helps you understand how the smartwatch haptic feedback system works and where each part of the system fits.

The system supports research studies where participants receive real-time haptic feedback through a Wear OS smartwatch. The watch collects sensor data and vibrates, the Android phone connects the watch to the backend, n8n processes the data and decides what feedback to send, PostgreSQL stores the system data, and the ResearcherSideApp gives you a dashboard for managing the study.



## **About the Smartwatch Haptic Feedback System**

The Smartwatch Haptic Feedback system is an experimental platform for delivering vibrotactile feedback through a Wear OS smartwatch. It combines a smartwatch sensing and vibration app, an Android phone relay, n8n automation workflows, a PostgreSQL database, and a ResearcherSideApp dashboard. Researchers can define use cases, configure feedback mappings, monitor participant data, and study how different haptic patterns support awareness, interpretation, and behavior during HCI experiments.

## **Key Features**

The system includes several connected components that support end-to-end haptic feedback experiments:

- **Smartwatch sensing and vibration**: The Wear OS app collects sensor data such as heart rate and executes vibration commands.
- **Android phone relay**: The phone app connects the watch to the backend, adds context such as GPS when needed, and relays backend haptic instructions back to the watch.
- **n8n automation backend**: Workflows receive data, call APIs, apply mapping logic, manage schedules and dictionary entries, and return vibration instructions.
- **PostgreSQL database**: Stores users, devices, use cases, haptic mapping rules, sensor data, alerts, schedules, and AI assistant context.
- **ResearcherSideApp dashboard**: Lets researchers manage users, rules, schedules, dictionary entries, data views, and AI-assisted actions.

# What the system does

At a high level:

1. You configure users, use cases, mappings, and schedules in the ResearcherSideApp.
2. The smartwatch collects sensor data from the participant.
3. The Android phone sends watch data and phone context to n8n.
4. n8n looks up the user's active mapping, applies the relevant logic, stores the result, and returns haptic instructions.
5. The phone forwards the haptic command to the watch.
6. The watch performs the vibration pattern.

# How to use these docs

Choose the component you are working with. If you want the full system picture, use System Architecture. If you want a focused explanation of how the parts talk to each other, use Communication Between Components. If you are preparing or running a study, start with ResearcherSideApp and then check the phone and smartwatch pages as needed. If you want to add a use case, use Adding a New Use Case.

# Github

- ResearcherSide Dashboard [LINK REMOVED FOR ANONYMITY] - Used to manage experiments that live on the system.
- Smartwatch Haptic App (Wear OS) [LINK REMOVED FOR ANONYMITY] - Wear OS application serves as the primary edge node for the system.
- Android Phone App [LINK REMOVED FOR ANONYMITY] - The client that consumes these endpoints.
- Haptic Backend [LINK REMOVED FOR ANONYMITY] - The automation layer



# System Components

[System Architecture](page-45.md)

[End-to-End System Installation](page-18.md)

[ResearcherSideApp](page-34.md)

[Android Phone App](page-08.md)

[Smartwatch App](page-44.md)

[n8n](page-27.md)

[Database](page-17.md)

[Communication Between Components](page-10.md)





# Guides

[Tutorial Videos [REMOVED FOR ANONYMITY]](page-46.md)

[Adding a New Use Case](page-01.md)

[Initial Installation - Phone & Watch](page-19.md)

[Setting Credentials On n8n](page-37.md)





# Features

[Schedules](page-35.md)

[Use Case Dictionary](page-47.md)

[Chat and Knowledge Assistant](page-09.md)

[Graphs and Data Review](page-29.md)

