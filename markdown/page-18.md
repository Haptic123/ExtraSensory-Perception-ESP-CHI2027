# End-to-End System Installation

This guide explains how to install the complete Smartwatch Haptic Feedback System on a clean environment and verify the full flow:

**Smartwatch sensor → Android phone → n8n backend → PostgreSQL → haptic mapping → phone → smartwatch vibration → ResearcherSideApp**

Use this page for a complete installation. The linked component pages provide screenshots, detailed UI instructions, and component-specific troubleshooting.

- Table of Contents
    
    1. System componentsRelated documentation2. Choose the installation typeRecommended handover installationDeveloper installation3. PrerequisitesServer computerDevicesAccounts and credentials4. Collect the required installation files5. Install and restore PostgreSQLMore information5.1 Install PostgreSQL5.2 Create the databaseCommand-line optionpgAdmin option5.3 Restore the database dumpCommand-line optionpgAdmin option5.4 Verify the database6. Install and configure n8n6.1 Install n8n6.2 Import the workflows6.3 Configure credentialsPostgreSQLOpenAISMTP/emailOther AI or external APIs6.4 Reconnect workflow references6.5 Test database access6.6 Activate the workflows7. Configure backend network accessOption A: Everything on the server computerOption B: Set up NgrokResearcherSide and the phone may use:Test the URL8. Install ResearcherSideAppOption A: Use the prepared executableOption B: Run from sourceVerify ResearcherSideDetailed guide9. Initial Installation - Phone & Watch10. Configure the participant in ResearcherSide11. Run the complete end-to-end test11.1 Start the services11.2 Check the watch11.3 Check the phone11.4 Check ResearcherSide11.5 Produce one sensor reading11.6 Verify each layerWatchPhonen8nPostgreSQLResearcherSide12. Test optional featuresAI researcher assistantMonitoring-stop alertsData exportExternal API use cases13. Common installation problemsResearcherSide does not loadImported workflows fail to call each otherPostgreSQL nodes failPhone cannot reach n8nPhone cannot find the watchReadings reach n8n but no vibration is returnedA haptic command is returned but the watch does not vibrateParticipant disappeared from an active viewAI assistant failsMonitoring-stop email is not received14. Maintenance rules15. Source repositories and detailed guidesSource repositoriesNotion documentation
    

---

# 1. System components

The system contains five main components:

1. **PostgreSQL database:** Stores participants, devices, use cases, mappings, schedules, sensor readings, alerts, and AI session information.
2. **n8n backend:** Receives sensor readings, queries the database, evaluates feedback mappings, stores results, returns haptic commands, and serves the ResearcherSide application.
3. **ResearcherSideApp:** Used to manage participants, use cases, mappings, schedules, monitoring, graphs, exports, and the AI researcher assistant.
4. **Android phone application:** Connects the smartwatch to n8n. It receives readings through Bluetooth, sends them to the backend, and returns vibration commands to the watch.
5. **Wear OS smartwatch application:** Collects sensor readings and performs the haptic feedback.

### Related documentation

- [Smartwatch Haptic Feedback Hub](page-48.md)
- [ResearcherSideApp Documentation](page-34.md)
- [Initial Installation – Phone & Watch](page-19.md)
- [Setting Credentials on n8n](page-37.md)

# 2. Choose the installation type

## Recommended handover installation

Use the prepared release files:

- Current PostgreSQL dump
- Exported n8n workflows
- ResearcherSide executable
- Android phone APK
- Wear OS watch APK

This is the recommended option for researchers and system operators.

## Developer installation

Build the applications from their source repositories:

- Backend and database [LINK REMOVED FOR ANONYMITY]
- ResearcherSideApp [LINK REMOVED FOR ANONYMITY]
- Android phone application [LINK REMOVED FOR ANONYMITY]
- Wear OS application [LINK REMOVED FOR ANONYMITY]

Use the developer installation when changing URLs, phone IDs, application logic, sensors, or haptic behavior.

# 3. Prerequisites

## Server computer

Install or prepare:

- Windows computer with administrator access
- PostgreSQL 18
- pgAdmin or PostgreSQL command-line tools
- Self-hosted n8n
- Java/JDK 17 or newer
- IntelliJ IDEA when building ResearcherSide from source
- Android Studio when building either Android application
- Android SDK 34
- Git, when cloning the repositories
- A stable network connection
- A reachable n8n webhook URL

## Devices

Prepare:

- Android 11 or newer phone
- Wear OS watch running Android API 30 or newer
- USB data cable for the phone
- Watch charger
- Phone and watch Bluetooth pairing
- Wi-Fi access for the phone and server
- Developer mode and debugging access when installing APKs manually

## Accounts and credentials

Prepare access to:

- PostgreSQL administrator account
- n8n administrator account
- OpenAI API account
- SMTP/email account for monitoring-stop alerts
- Any external APIs used by enabled use cases
- Public tunnel, domain, or server configuration when operating outside the local network

> 🔐 Never store database passwords, OpenAI keys, SMTP passwords, or private API keys in GitHub, exported workflow JSON files, screenshots, or this Notion page.
> 

# 4. Collect the required installation files

Before beginning, create one installation folder containing:

```
Smartwatch-Haptic-Installation/
├── Database/
│   └── DB-18072026.sql
├── n8n-Workflows/
│   ├── DB Manager.json
│   ├── Vibration Orchestrator.json
│   ├── Chat Orchestrator.json
│   ├── Mapping Manager.json
│   ├── Schedule Manager.json
│   ├── Dictionary Manager.json
│   ├── Use Case Builder.json
│   ├── Knowledge Agent.json
│   ├── Expert Panel Agent.json
│   └── Agent Expert - [...].json
└─ Applications/
   ├── ResearcherSideApp.exe
   ├── PhoneApp.apk
   └── WatchApp.apk
```

The workflow repository may contain additional root-level JSON files. Import **all current root-level workflow files**, not only the three public entrypoints.

---

# 5. Install and restore PostgreSQL

### More information

See the database setup and operations section in the [Database](page-17.md).

## 5.1 Install PostgreSQL

Install **PostgreSQL 18**, including:

- PostgreSQL Server
- pgAdmin
- Command Line Tools

Record the following securely:

- Host
- Port
- Administrator username
- Administrator password

The default local values are usually:

```
Host: localhost
Port: 5432
Username: postgres
```

## 5.2 Create the database

Create a database named:

```
smartwatchsys_db
```

### Command-line option

```bash
createdb -U postgres smartwatchsys_db
```

### pgAdmin option

1. Open pgAdmin.
2. Connect to the PostgreSQL server.
3. Right-click **Databases**.
4. Select **Create → Database**.
5. Enter `smartwatchsys_db`.
6. Save.

## 5.3 Restore the database dump

### Command-line option

Run the command from the folder containing the SQL file:

```bash
psql -U postgres -d smartwatchsys_db -f DB-18072026.sql
```

### pgAdmin option

1. Select `smartwatchsys_db`.
2. Open **Query Tool**.
3. Load `DB-18072026.sql`.
4. Execute the file.
5. Wait for completion.
6. Review the Messages panel for errors.

## 5.4 Verify the database

Confirm that the database contains tables including:

- `User`
- `Watch`
- `AndroidPhone`
- `UseCase`
- `UseCaseDictionary`
- `feedback_config_rules`
- `User_UC_Mappings`
- `SensorData`
- `Alert`
- `user_schedules`
- `agent_session`

Also verify that database functions such as the ‘*resolve_fb_range*’ and ‘*insert_sensor_data*’ functions were created.

> ✅ **Verification gate:** The schema is visible, existing use cases can be queried, and no critical errors appeared during restoration.
> 
> 
> **Verification gate:**
> 

---

# 6. Install and configure n8n

## 6.1 Install n8n

Install the validated n8n version listed at the top of this page. [LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY]

After installation:

1. Start n8n.
2. Open the n8n editor.
3. Create or sign in to the administrator account.
4. Confirm that the editor loads correctly.

The default local address is generally:

```
[LINK REMOVED FOR ANONYMITY]
```

## 6.2 Import the workflows

Import every current root-level `.json` workflow from the backend repository or installation package. Read more about workflows [n8n Workflows Breakdown](page-23.md)

The main public workflows are:

- `DB Manager`
- `Vibration Orchestrator`
- `Chat Orchestrator`

Supporting workflows include:

- `Mapping Manager`
- `Schedule Manager`
- `Dictionary Manager`
- `Use Case Builder`
- `Expert Panel Agent`
- The `Agent Expert` workflows
- `Knowledge Agent` [DEPRECATED]


💡 Do not activate them yet.



## 6.3 Configure credentials

Configure every credential referenced by the imported workflows.

For detailed credential instructions, open:

- [Setting Credentials on n8n](page-37.md)
- n8n PostgreSQL documentation [LINK REMOVED FOR ANONYMITY]
- n8n OpenAI credentials [LINK REMOVED FOR ANONYMITY]
- n8n Google AI credentials [LINK REMOVED FOR ANONYMITY]
- n8n Send Email credentials [LINK REMOVED FOR ANONYMITY]

### PostgreSQL

Point all PostgreSQL credential references to:

```
Host: localhost
Port: 5432
Database: smartwatchsys_db
User: [PostgreSQL user]
Password: [PostgreSQL password]
```

### OpenAI

Configure the OpenAI credential used by the chat and AI-agent workflows.

### SMTP/email

Configure SMTP credentials when monitoring-stop email alerts are enabled.

### Other AI or external APIs

Configure Google AI or additional API credentials only when they are referenced by the imported workflow version.

## 6.4 Reconnect workflow references

> ⚠️ **Do not skip this step.**
> 
> 
> **Do not skip this step.**
> 

Imported workflow IDs can differ from the IDs stored in exported files.

Open every node of the following types:

- **Execute Workflow**
- Workflow tools used by AI agents
- Any node that selects another workflow by ID

Re-select the intended target workflow from the dropdown, even when a workflow name already appears.

Pay particular attention to links between:

- Orchestrators and manager workflows
- Chat Orchestrator and AI workflows
- Knowledge and expert-panel workflows
- Use Case Builder and dictionary/mapping workflows

A workflow may import successfully but still fail at runtime when these references are not reconnected.

## 6.5 Test database access

Run a safe database-reading node or connection-check endpoint.

Confirm:

- PostgreSQL credentials authenticate successfully.
- `smartwatchsys_db` is selected.
- Existing participants or use cases are returned.
- No credential or SQL errors appear.

## 6.6 Activate the workflows

At minimum, activate:

- `DB Manager`
- `Vibration Orchestrator`
- `Chat Orchestrator`

Activate the supporting workflows required by the current workflow design.

> ✅ **Verification gate:** The production webhooks are registered, PostgreSQL queries succeed, and all Execute Workflow nodes point to valid workflows.
> 
> 
> **Verification gate:**
> 

---

# 7. Configure backend network access

The correct URL depends on where the clients are running.

## Option A: Everything on the server computer

ResearcherSide may use:

```
[LINK REMOVED FOR ANONYMITY]
```

The phone cannot use `localhost`, because `localhost` on the phone refers to the phone itself.

## Option B: Set up Ngrok

Expose your local n8n server to the internet so that both the phone app and the researcher dashboard can communicate with it from outside the local network.

1. Install Ngrok [LINK REMOVED FOR ANONYMITY] and sign up for a free account to get an authentication token.
2. Authenticate your Ngrok CLI in your terminal:
    
    ```bash
    ngrok config add-authtoken <your_auth_token>
    ```
    
3. Start the tunnel to forward traffic to the local n8n instance (port `5678`):
    
    ```bash
    ngrok http 5678
    ```
    
4. Copy the generated public `https` URL from the terminal output (e.g., `[LINK REMOVED FOR ANONYMITY]).

Both the phone app and the researcher dashboard must use this address:

#### ResearcherSide and the phone may use:

```
https://<your-subdomain>.ngrok-free.app/webhook
```

## Test the URL

From another device on the intended network, call a safe connection-check endpoint.

Confirm that:

- The host resolves.
- HTTPS certificates are accepted when using HTTPS.
- The request reaches n8n.
- The expected workflow executes.
- The response is not an n8n editor page or tunnel warning page.

Record the final base URL at the top of this document.

---

# 8. Install ResearcherSideApp

## Option A: Use the prepared executable

1. Copy the current ResearcherSide release folder to the server computer.
2. Keep any included libraries or configuration files beside the executable.
3. Confirm that the application is configured for the correct n8n production URL.
4. Start the application.
5. Allow it through Windows Firewall if prompted.

The recommended setup is to run ResearcherSide on the same computer as n8n, using:

```
[LINK REMOVED FOR ANONYMITY]
```

## Option B: Run from source

1. Clone or download the ResearcherSide repository [LINK REMOVED FOR ANONYMITY].
2. Install JDK 17 or newer with JavaFX support.
3. Open the project in IntelliJ IDEA.
4. Add the bundled root-level JAR files to the module classpath.
5. Open:

```
com/example/demo/service/ApiService.java
```

1. Set the n8n production webhook URL.
2. Run:

```
com.example.demo.SmartWatchHapticSystemApplication
```

## Verify ResearcherSide

Confirm that:

- The initial n8n connection check succeeds.
- The dashboard loads.
- Participants and use cases are visible.
- Mapping and schedule pages load.
- No database credentials are requested by the desktop application.

ResearcherSide communicates with n8n and does not connect directly to PostgreSQL.

### Detailed guide

Open the [ResearcherSideApp Documentation](page-34.md).

> ✅ **Verification gate:** ResearcherSide opens, passes its backend connection check, and loads database-backed information.
> 
> 
> **Verification gate:**
> 

---

# 9. Initial Installation - Phone & Watch

Before configuring the applications, determine:

- Participant/user ID
- Smartwatch ID
- Android phone ID
- Assigned use case
- Active feedback mapping

Example:

```
User ID: 1
Smartwatch ID: 1
Android Phone ID: 50
```

The identifiers used by the watch name, phone application, database, and ResearcherSide must refer to the same participant-device assignment.

For the full detailed guide: [Initial Installation - Phone & Watch](page-19.md)

---

# 10. Configure the participant in ResearcherSide

After the applications and backend are available:

1. Open ResearcherSide.
2. Create or select the intended participant.
3. Confirm that the participant ID matches the watch Bluetooth name.
4. Confirm that the Android phone and smartwatch IDs match the configured devices.
5. Assign the required use case.
6. Assign an active feedback mapping.
7. Review the mapping ranges and haptic parameters.
8. Configure a schedule when the use case requires one.
9. Confirm that the participant has an active monitoring configuration.

The active mapping must define the appropriate values for:

- Minimum and maximum sensor values
- Pulses
- Intensity
- Duration
- Interval

> ⚠️ Confirm that the assigned mapping is active. A participant assigned only to an inactive mapping may not appear correctly in active views and will not receive the expected feedback.
> 

For exact interface instructions, use the mapping, monitoring, scheduling, and participant sections of the [ResearcherSideApp Documentation](page-34.md).

---

# 11. Run the complete end-to-end test

Use test IDs or a designated test participant rather than an active research participant.

## 11.1 Start the services

Start in this order:

1. PostgreSQL
2. n8n
3. Required active n8n workflows
4. ResearcherSide
5. Wear OS application
6. Android phone application

## 11.2 Check the watch

Confirm:

- Correct Bluetooth name
- Body-sensor permission granted
- Bluetooth permission granted
- Application running
- Foreground notification visible
- Battery sufficient

## 11.3 Check the phone

Confirm that the diagnostics show:

- Bluetooth connected
- n8n connected
- Location available when required
- Correct monitoring type
- Foreground monitoring service active

## 11.4 Check ResearcherSide

Confirm:

- Correct participant selected
- Correct use case selected
- Active mapping assigned
- Monitoring enabled
- Expected schedules visible

## 11.5 Produce one sensor reading

Start monitoring and wait for one reading.

The expected route is:

```
Watch
→ Bluetooth sensor message
→ Android phone
→ POST /webhook/usecase-routing
→ Vibration Orchestrator
→ Database lookup and mapping evaluation
→ SensorData and Alert records
→ Haptic response
→ Android phone
→ Vibrate command
→ Watch vibration
```

## 11.6 Verify each layer

### Watch

- A sensor reading was produced.
- A vibration was received.

### Phone

- The sensor message contains the expected IDs.
- The n8n request succeeded.
- A haptic response was received.
- The vibration command was sent to the watch.

### n8n

- The correct production workflow executed.
- No node failed.
- The correct use-case branch was selected.
- An active mapping was found.
- A haptic result was generated.

### PostgreSQL

Verify that the test created or updated the expected records in:

- `SensorData`
- `Alert`

### ResearcherSide

- The new reading appears.
- The feedback event appears.
- The graph updates.
- The participant remains connected.

> ✅ **Installation success:** The test sensor value reaches the backend and database, appears in ResearcherSide, and causes the expected watch vibration.
> 
> 
> **Installation success:**
> 

---

# 12. Test optional features

After the main sensor-to-vibration flow succeeds, test each enabled optional feature separately.

## AI researcher assistant

Confirm:

- `Chat Orchestrator` is active.
- OpenAI credentials are valid.
- Supporting agent workflows are connected.
- A basic participant or mapping question returns an answer.
- A write action is tested only with safe test data.

## Monitoring-stop alerts

Confirm:

- SMTP credentials are configured.
- The stopped-monitoring webhook is active.
- A test stop event reaches `DB Manager`.
- The expected email is received.

## Data export

Confirm that ResearcherSide can export:

- CSV
- PDF

Open the exported files and verify that the participant, timestamps, readings, and feedback information are correct.

## External API use cases

For each enabled API-based use case:

- Verify the API credential or token.
- Verify required parameters such as coordinates.
- Run one test request.
- Confirm a numeric value reaches the mapping stage.
- Confirm the corresponding feedback is stored and returned.

---

# 13. Common installation problems

## ResearcherSide does not load

Check:

- PostgreSQL is running.
- n8n is running.
- `DB Manager` is active.
- `ApiService.java` or the packaged application points to the correct URL.
- The URL ends with `/webhook`.
- The connection-check endpoint responds.

## Imported workflows fail to call each other

Likely cause:

- Exported workflow IDs no longer match the imported workflow IDs.

Fix:

- Open every Execute Workflow or workflow-tool node.
- Re-select the target workflow.
- Save the workflow.
- Test it again.

## PostgreSQL nodes fail

Check:

- Database name is `smartwatchsys_db`.
- PostgreSQL service is running.
- Host and port are correct.
- Username and password are correct.
- Both imported PostgreSQL credentials point to the restored database.
- The current SQL dump was completely restored.

## Phone cannot reach n8n

Check:

- The phone is not using `localhost`.
- The configured URL includes `/webhook`.
- The workflow is active.
- The phone can reach the server network address.
- Windows Firewall permits the connection.
- The HTTPS certificate is valid.
- Local HTTP access is allowed in `network_security_config.xml` when applicable.

## Phone cannot find the watch

Check:

- Phone and watch are paired.
- The watch name follows the required format.
- The name contains `SmartWatchID`.
- Bluetooth permissions are granted.
- The watch app is running.
- Remove conflicting paired watches during testing.

## Readings reach n8n but no vibration is returned

Check:

- Correct participant ID
- Correct watch and phone IDs
- Active monitoring type
- Active use case
- Active mapping assignment
- Sensor value falls within a configured mapping range
- Mapping intensity, pulses, and duration are positive
- Rate-limit or smoothing behavior
- Workflow execution errors

## A haptic command is returned but the watch does not vibrate

Check:

- Phone Bluetooth connection
- Watch application and foreground service
- Watch vibration permission and device settings
- Haptic intensity is no greater than `255`
- Pulses, intensity, and duration are positive
- Phone log confirms that the `Vibrate` command was sent

## Participant disappeared from an active view

Check:

- The participant still has an active assignment.
- The assigned mapping is active.
- The participant was reassigned when an old mapping was deactivated or deleted.
- Show All and assignment-history views before changing database records manually.

## AI assistant fails

Check:

- OpenAI credentials
- Model access and available balance
- `Chat Orchestrator`
- Agent workflow references
- Required vector-store or context configuration
- Failed n8n execution logs

## Monitoring-stop email is not received

Check:

- SMTP credentials
- Recipient configuration
- `DB Manager`
- Stopped-monitoring webhook execution
- Spam folder
- Email provider security restrictions

---

# 14. Maintenance rules

Whenever the system changes:

- **Backend URL changed:** update the phone application and ResearcherSide configuration.
- **Phone ID changed:** update both the phone build and database assignment.
- **Watch or user changed:** update the Bluetooth alias and database records.
- **Workflows imported again:** re-select all workflow references.
- **Database schema changed:** create a new dump and update this page.
- **Use case added:** keep its name identical across the database, dictionary, n8n, phone/watch logic, and ResearcherSide.
- **APK or EXE rebuilt:** archive the old version and update the version manifest.
- **Credentials rotated:** update n8n credentials and rerun the relevant tests.
- **Tunnel or domain changed:** verify all client applications before the next session.

---

# 15. Source repositories and detailed guides

## Source repositories

- Smartwatch Haptic Workflow Backend [LINK REMOVED FOR ANONYMITY]
- ResearcherSideApp [LINK REMOVED FOR ANONYMITY]
- Android Phone Haptic Relay [LINK REMOVED FOR ANONYMITY]
- Smartwatch Haptic App [LINK REMOVED FOR ANONYMITY]

## Notion documentation

- [Smartwatch Haptic Feedback Hub](page-48.md)
- [Initial Installation – Phone & Watch](page-19.md)
- [ResearcherSideApp Documentation](page-34.md)
- [Setting Credentials on n8n](page-37.md)