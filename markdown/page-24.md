# n8n Webhook Tests Breakdown

> This is a test page for future developers. It keeps the commands that provide useful coverage of the main system features and removes repetitive variants that test the same workflow branch.
> 

## **How to run the curl commands correctly**

1. **Make sure n8n is running.** These commands use `[LINK REMOVED FOR ANONYMITY] so the n8n instance must be available on the same computer. If n8n is hosted elsewhere, replace the base address with the correct server address.
2. **Make sure the relevant workflow is active.** Commands using `/webhook/` call an active workflow.
3. **For testing inside the n8n editor**, click **Listen for test event** in the workflow and replace `/webhook/` with `/webhook-test/` in the command.
4. **Open PowerShell** and paste the entire command on one line. The examples use `curl.exe`, which calls the normal Windows curl program instead of the PowerShell alias.
5. **Replace every placeholder before running the command.** Examples include:
    - `<USER_ID>`
    - `<MAPPING_ID>`
    - `<SCHEDULE_ID>`
6. **Use test records whenever possible.** Commands marked as changing data can create, update, activate, deactivate, reassign, or log information. Do not run them on important production records unless the change is intended.
7. **Run one state-changing command at a time.** Check the response and the database before continuing, especially when testing mapping or schedule changes.
8. **Use a new `session_id` for separate chat tests.** This prevents old chat history from affecting the new test.
9. **Allow time between sensor-routing tests.** The Vibration Orchestrator may rate-limit repeated requests. Environmental tests may also fail when an external service is unavailable.
10. **Read the HTTP status shown at the top of the response.**
    - `2xx` normally means the request succeeded.
    - `400` normally means the request was rejected because the input was invalid.
    - `404` means the requested record or route was not found.
    - `409` means the request conflicts with the current data.
    - `5xx` usually means a workflow, database, or external-service error.

### **What the curl options mean**

- `i` includes the HTTP status and response headers.
- `sS` hides the progress meter but still shows errors.
- `X` sets the request type, such as `GET` or `POST`.
- `H` adds a request header.
- `d` sends JSON data to the webhook.

## **Safety labels**

- **🟢 READ-ONLY** — should not intentionally change application data.
- **🟡 CHANGES DATA** — creates, updates, activates, deactivates, reassigns, or logs data.
- **🔵 EXTERNAL SERVICE / AI** — contacts an external API or AI model and may also save execution or session data.

---

## **1. Basic system and database checks**

### **Check that the DB Manager webhook is reachable**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Use this first when the application cannot reach n8n. It checks whether the main DB Manager webhook is available and can return a normal response.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY]
```

### **Get the current feedback configurations**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Shows the rules that connect sensor values to vibration behavior. This helps confirm that the application can load the available mappings.

```powershell
curl.exe -i -sS -X GET "[LINK REMOVED FOR ANONYMITY]
```

### **Get users and their active mappings**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Shows every user together with the use case and feedback rule currently assigned to that user. This is useful when a user appears to have the wrong configuration.

```powershell
curl.exe -i -sS -X GET "[LINK REMOVED FOR ANONYMITY]
```

### **Get the available sensor and use-case types**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Shows the use cases stored in the system, such as HeartRate. Run this when a use case is missing from the interface or cannot be selected.

```powershell
curl.exe -i -sS -X GET "[LINK REMOVED FOR ANONYMITY]
```

### **Get HeartRate sensor data**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Checks whether saved HeartRate readings for user 100 can be found and returned correctly. Change the user ID when testing another user.

```powershell
curl.exe -i -sS -X GET "[LINK REMOVED FOR ANONYMITY]
```

### **Get a user's mapping history**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Shows both current and previous HeartRate mapping assignments for user 100. This helps explain when and how a user's assignment changed.

```powershell
curl.exe -i -sS -X GET "[LINK REMOVED FOR ANONYMITY]
```

## **2. Monitoring state**

### **Get a user's monitoring configuration**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Returns the monitoring setup for user 100. It also marks monitoring as expected, clears the offline-alert flag, and updates the user's last request time.

```powershell
curl.exe -i -sS -X GET "[LINK REMOVED FOR ANONYMITY]
```

### **Stop monitoring intentionally**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Tells the system that user 100 stopped monitoring on purpose. This prevents the system from treating the stop as an unexpected offline event.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"userId":100,"reason":"user_stopped"}'
```

## **3. Use cases and feedback mappings**

### **Create a new use case**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Creates a temporary use case and checks whether name validation and database insertion work. Change the name before running the command again.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"name":"CurlTestUseCase","description":"Temporary use case created by the webhook curl catalog"}'
```

### **Assign a use case to a user**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Assigns use case 3 to user 100. The workflow may reuse a previous mapping or choose an active default mapping for that use case.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"userId":100,"usecaseId":3}'
```

### **Activate an existing mapping**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Makes an existing feedback rule available for use. Replace the placeholder with a mapping ID returned by the current-configurations test.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"mappingId":<MAPPING_ID>,"active":true}'
```

### **Deactivate a mapping and handle affected users**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Turns off a mapping. The workflow should move affected users to another suitable mapping, or return a conflict response when no replacement exists.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"mappingId":<MAPPING_ID>,"active":false}'
```

### **Insert a feedback rule through set-rules**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Creates a HeartRate feedback rule using the special nested-list format required by this endpoint. This is especially useful after changes to the rule-import workflow.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '[[{"type":"HeartRate","minvalue":60,"maxvalue":100,"minpulses":1,"maxpulses":3,"minintensity":20,"maxintensity":60,"minduration":100,"maxduration":300,"mininterval":200,"maxinterval":600,"active":true}]]'
```

### **Assign an existing mapping through mapping-commands**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Checks the command path used to assign a specific mapping to a specific user. Replace both placeholders with real test records.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"action":"assign_mapping_to_user","mapping_id":<MAPPING_ID>,"user_id":<USER_ID>,"usecase_id":3,"usecase_name":"HeartRate","session_id":"curl-mapping-assign"}'
```

### **Change a mapping for all assigned users**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Changes one vibration setting in a shared mapping. Because the mapping is shared, every user assigned to it may be affected.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"action":"change","usecase_id":3,"usecase_name":"HeartRate","session_id":"curl-mapping-change","params":{"id":<MAPPING_ID>,"minpulses":2}}'
```

### **Create a user-specific mapping copy**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Copies an existing mapping, changes the copied value, and assigns the copy only to one user. Other users keep the original mapping.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"action":"duplicate_mapping_for_user","original_mapping_id":<MAPPING_ID>,"user_id":<USER_ID>,"usecase_id":3,"usecase_name":"HeartRate","session_id":"curl-mapping-duplicate","params":{"minpulses":3}}'
```

### **Reject an unsupported mapping command**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Checks that the system refuses an unknown command instead of sending it to the Mapping Manager. A correct result is an HTTP 400 response.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"action":"unsupported","usecase_id":3,"usecase_name":"HeartRate"}'
```

## **4. Schedule management**

### **List all schedules for a use case**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Shows both active and inactive HeartRate schedules. Run this before changing a schedule so you can find the correct schedule ID.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"action":"listAll","usecase_name":"HeartRate","session_id":"curl-schedule-list-all","params":{"user_id":100}}'
```

### **Add a schedule**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Creates a HeartRate schedule for user 100 that runs every seven days. It also checks whether the next run date is calculated correctly.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"action":"add","usecase_name":"HeartRate","session_id":"curl-schedule-add","params":{"user_id":100,"interval_days":7,"measure_type":"average","trigger_percentage":10}}'
```

### **Change a schedule**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Updates an existing schedule's timing, calculation method, trigger level, and next run date. Replace the placeholder with a real schedule ID.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"action":"change","usecase_name":"HeartRate","session_id":"curl-schedule-change","params":{"schedule_id":<SCHEDULE_ID>,"user_id":100,"interval_days":14,"measure_type":"median","trigger_percentage":15}}'
```

### **Deactivate a schedule**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Turns off one schedule without deleting it. The workflow also checks that the schedule belongs to the selected use case.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"action":"deactivate","usecase_name":"HeartRate","session_id":"curl-schedule-deactivate","params":{"schedule_id":<SCHEDULE_ID>}}'
```

### **Activate a schedule**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Turns a schedule back on. The workflow also turns off other schedules for the same use case so that only the intended schedule remains active.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"action":"activate","usecase_name":"HeartRate","session_id":"curl-schedule-activate","params":{"schedule_id":<SCHEDULE_ID>}}'
```

## **5. Sensor routing and vibration generation**

### **Route a HeartRate reading**

**Safety:** 🟡 CHANGES DATA

**What this test is useful for:** Sends a HeartRate value through the full sensor workflow. It checks the selected rule, the vibration result, rate limits, and sensor-data logging.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"userId":100,"smartWatchId":200,"androidId":2,"type":"HeartRate","value":82}'
```

### **Route a Temperature request**

**Safety:** 🔵 EXTERNAL SERVICE + CHANGES DATA

**What this test is useful for:** Gets the temperature for the supplied location, then uses it to calculate vibration feedback and log the result. It also checks the connection to the weather service.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"userId":100,"smartWatchId":200,"androidId":2,"type":"Temperature","lat":32.794,"lon":34.989}'
```

### **Route a Pollution request**

**Safety:** 🔵 EXTERNAL SERVICE + CHANGES DATA

**What this test is useful for:** Gets air-quality information for the supplied location, applies the pollution feedback rule, and logs the result. It checks a different external service from the weather test.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"userId":100,"smartWatchId":200,"androidId":2,"type":"Pollution","lat":32.794,"lon":34.989}'
```

### **Reject an unsupported sensor type**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Sends a sensor type that the system does not support. The workflow should return its fallback response instead of trying to process the value.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"userId":100,"smartWatchId":200,"androidId":2,"type":"UnsupportedCurlType","value":42}'
```

### **Reject a sensor request with missing device IDs**

**Safety:** 🟢 READ-ONLY

**What this test is useful for:** Checks that the workflow refuses a request when the smartwatch and Android device IDs are missing. This confirms that required input is being checked.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"userId":100,"type":"HeartRate","value":82}'
```

## **6. AI chat routing**

### **Test participant-level chat analysis**

**Safety:** 🔵 EXTERNAL AI + SAVES SESSION DATA

**What this test is useful for:** Asks the AI to explain the current HeartRate mapping for one participant without changing it. It checks participant context, AI routing, and chat-history storage.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"session_id":"curl-chat-participant","usecase_id":3,"usecase_name":"HeartRate","user_id":100,"user_name":"Curl Test User","analysis_scope":"participant","message":"Explain the current HeartRate mapping for this participant without changing anything."}'
```

### **Test use-case-wide chat analysis**

**Safety:** 🔵 EXTERNAL AI + SAVES SESSION DATA

**What this test is useful for:** Asks the AI to summarize HeartRate mappings across the whole use case. It checks the all-users analysis path and chat-history storage.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"session_id":"curl-chat-usecase","usecase_id":3,"usecase_name":"HeartRate","all_users_selected":true,"analysis_scope":"usecase","message":"Summarize the active HeartRate mappings without changing anything."}'
```

### **Reject incomplete chat input**

**Safety:** 🔵 MAY REACH AI VALIDATION PATH

**What this test is useful for:** Leaves out the required use-case ID. The request should be rejected, confirming that incomplete chat requests cannot continue through the normal workflow.

```powershell
curl.exe -i -sS -X POST "[LINK REMOVED FOR ANONYMITY] -H "Content-Type: application/json" -d '{"session_id":"curl-chat-invalid","message":"This request intentionally omits the use-case ID."}'
```

---

## **Tests intentionally left out**

The full webhooks available contain additional commands for alternate sensor-data query formats, extra validation cases, and every supported environmental sensor type. They were not repeated here because they follow the same main workflow paths as the selected tests.

The selected **Temperature** test represents the weather-data path, while **Pollution** represents a separate air-quality service. The selected **HeartRate** test covers direct sensor values supplied by the device.