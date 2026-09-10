# Setting Credentials On n8n

> This page explains which credentials must be configured in **n8n** for the SmartWatch Haptic backend, and where each credential is used.
> 
> 
> It is not a full credential setup tutorial. For detailed setup screens, use the official n8n documentation linked below.
> 

---

## ✅ Required Credentials

The project mainly uses these n8n credentials:

| Credential | Used For | n8n Docs |
| --- | --- | --- |
| [**Postgres**](page-37.md) | Reading and writing sensor data, users, mappings, feedback rules, alerts | Postgres node docs [LINK REMOVED FOR ANONYMITY] |
| [**OpenAI**](page-37.md) | AI Agent / LLM-based analysis and assistant responses | OpenAI credentials docs [LINK REMOVED FOR ANONYMITY] |
| [**Google Gemini / Google AI**](page-37.md) | Alternative LLM provider for AI Agent / Gemini Chat Model nodes | Google AI credentials docs [LINK REMOVED FOR ANONYMITY] |
| [Send Email SMTP Account](page-37.md) | Sending emails | [LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY] |

> n8n credentials are private connection settings used by nodes to authenticate with external services. The Credentials screen is available from the left menu in n8n.
> 

---

## 🗄️ Postgres Credential

The **Postgres credential** connects n8n to the project database.

In this project, Postgres is used for:

- Fetching active feedback mapping rules
- Saving sensor readings
- Saving generated alerts
- Reading user/use-case mapping data
- Supporting ResearcherSide data queries

> The database used in the project setup is named:
> 
> 
> `smartwatchsys_db`
> 

From the project setup instructions, the PostgreSQL connection settings are generally:

```
Host: localhost
Port: 5432
Database: smartwatchsys_db
User: postgres
Password: your PostgreSQL password
```

The password should be the one chosen during PostgreSQL installation, and that changing the shared PostgreSQL configuration node updates the connection for the relevant flow nodes.

> Do not keep the default placeholder password in production. Use the real password from the PostgreSQL installation.
> 

Official docs:

[LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY]

---

## 🤖 OpenAI Credential

The **OpenAI credential** is used when the workflow contains OpenAI-based nodes, such as:

- OpenAI
- Chat OpenAI
- Embeddings OpenAI
- LM OpenAI

n8n’s OpenAI credential uses an **API key** authentication method.

> Use OpenAI credentials when the workflow needs GPT-based analysis, natural-language responses, or agent reasoning.
> 

Official docs:

[LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY]

---

## ✨ Google Gemini / Google AI Credential

The **Google Gemini / Google AI credential** is used when the workflow contains Gemini nodes, such as:

- Google Gemini
- Google Gemini Chat Model
- Embeddings Google Gemini
- Google Gemini / PaLM-related nodes

n8n’s Google Gemini credential uses an API key from **Google AI Studio**. The n8n docs describe creating an API key in Google AI Studio and pasting it into the n8n credential.

> Use this credential if the AI Agent or chat model node is configured to use Gemini instead of OpenAI.
> 

Official docs:

[LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY]

---

## 📧 Send Email Credential

The **Send Email credential** is used when the workflow needs to send emails from n8n, for example:

- Monitoring stopped alerts
- System/admin notifications
- Researcher-side status emails
- Error or retry-limit notifications

n8n’s **Send Email** credential uses an **SMTP account**. To configure it, you generally need the sender email address, password or app password, SMTP host, port, and SSL/TLS settings. n8n notes that some providers require enabling outgoing SMTP or generating an app password first.

> For Gmail, n8n recommends using an **app password**, with:
> 
> 
> ```
> Host: smtp.gmail.com
> Port: 465 for SSL
> Port: 587 for TLS
> SSL/TLS: ON for port 465
> ```
> 

> Outlook.com / Microsoft 365 accounts no longer work with the Send Email node using basic username/password or app-password SMTP authentication. n8n recommends using the **Microsoft Outlook node** instead, because it uses OAuth 2.0.
> 

Official docs:

[LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY]

---

## 🧩 Where Credentials Are Used in the Workflow

| Workflow Area | Credential Needed |
| --- | --- |
| Heart rate data flow | Postgres |
| Sun / Moon / environmental API mapping flows | Postgres |
| Feedback rule lookup | Postgres |
| SensorData / Alert insert flow | Postgres |
| ResearcherSide mapping/history queries | Postgres |
| AI Agent responses | OpenAI or Google Gemini |
| LLM-powered use-case or mapping suggestions | OpenAI or Google Gemini |

> The backend workflow includes Postgres nodes such as feedback rule loading, heart-rate history fetching, and sensor-data insertion. These nodes depend on the Postgres credential being valid.
> 

---

## 🧪 Quick Credential Test

After creating or updating credentials:

1. Open a node that uses the credential.
2. Select the relevant credential from the credential dropdown.
3. Click **Test step** or run the workflow in test mode.
4. Confirm that the node returns data and does not show an authentication error.

> Common Issues
> 
> 
> If a Postgres node fails, check:
> 
> - PostgreSQL is running
> - Host and port are correct
> - Database name is correct
> - Username and password are correct
> - The selected n8n credential is the one used by the node
> - The database schema was imported correctly

---

## 🔒 Security Notes

> Never paste API keys or database passwords into:
> 
> - GitHub repositories
> - screenshots
> - public Notion pages
> - exported workflow files shared publicly
> - frontend Android code

Use n8n credentials instead of hardcoding secrets inside Code nodes whenever possible.

---

## 📚 Official References

- Postgres node: [LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY]
- OpenAI credentials: [LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY]
- Google AI / Gemini credentials: [LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY]
- Send Email credentials: [LINK REMOVED FOR ANONYMITY] [LINK REMOVED FOR ANONYMITY]

[For credential setup, open the Setting Credentials on n8n page.](page-36.md)