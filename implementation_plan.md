# FlowZint — n8n AI Workflows Implementation Plan

This plan outlines the generation of comprehensive, import-ready n8n workflow JSON files for FlowZint's AI Automation system. These workflows coordinate the entire lead lifecycle, bridging the **FastAPI Backend**, the **AI Agents (powered by Groq)**, and third-party communication tools (**Gmail**, **Google Calendar**, and **WebSockets**).

---

## User Review Required

> [!IMPORTANT]
> The generated n8n workflows rely on two global n8n variables:
> 1. `FASTAPI_URL` (e.g., `https://your-backend.railway.app`)
> 2. `FRONTEND_URL` (e.g., `https://flowzint.vercel.app`)
>
> You must define these variables in your n8n settings (**Settings → Variables**) before executing the workflows.
>
> Additionally, you will need to establish the following credentials in your n8n instance:
> - **Google Calendar OAuth2 API** (for scheduling)
> - **Gmail OAuth2 API** (for outreach, nurture, and scheduler confirmations)
> - **HTTP Header Auth** named `Header Auth credential` containing the header `Authorization` with value `Bearer <your_app_secret_from_env>` to authenticate with FastAPI.

---

## Proposed Changes

We will create a new directory `n8n` in your workspace (`d:\FlowZint\n8n`) containing importable JSON files for each of the six workflows.

### [Component] n8n Workflows (`d:\FlowZint\n8n`)

#### [NEW] [workflow_1_lead_intake.json](file:///d:/FlowZint/n8n/workflow_1_lead_intake.json)
Handles incoming webhook lead registration, triggers lead scoring & qualification via the FastAPI Qualifier Agent, and routes the lead based on their intent (High, Medium, Low).
- **Nodes**: Webhook, Create Execution Record, Qualify Lead, Switch (Route by Intent), Notify High Intent, Wait 1 Hour, Notify Low Intent, Trigger Outreach.

#### [NEW] [workflow_2_outreach.json](file:///d:/FlowZint/n8n/workflow_2_outreach.json)
Generates personalized outreach copy via the Outreach Agent, sends the email, waits for a reply, and analyzes the response sentiment/objection.
- **Nodes**: Webhook (outreach-start), Generate Outreach, Send Email, Notify Email Sent, Wait for Reply (48h Webhook-based wait), Analyze Sentiment, Switch (Route by Reply), Trigger Scheduler, Trigger Negotiation.

#### [NEW] [workflow_3_negotiation.json](file:///d:/FlowZint/n8n/workflow_3_negotiation.json)
Manages customer objections (price, timing, trust) by calling the Negotiation Agent, emailing back, and scheduling a follow-up check.
- **Nodes**: Webhook (negotiate), Handle Objection, Send Response Email, Notify Negotiation, Wait for Second Reply (24h), Check if Interested, Trigger Scheduler, Trigger Follow-up.

#### [NEW] [workflow_4_followup.json](file:///d:/FlowZint/n8n/workflow_4_followup.json)
A daily cron and API-triggered agent that scans the database for cold/stale leads (no contact > 3 days) and reaches out via the Follow-up Agent.
- **Nodes**: Schedule Trigger (10 AM), Webhook (followup-start), Get Stale Leads, Split In Batches, Generate Follow-up, Send Follow-up, Notify Dashboard, Loop Controller.

#### [NEW] [workflow_5_scheduler.json](file:///d:/FlowZint/n8n/workflow_5_scheduler.json)
Handles booking requests by finding optimal calendar slots via the Scheduler Agent, creating Google Calendar events, and emailing confirmations.
- **Nodes**: Webhook (schedule-meeting), Find Best Time, Create Calendar Event, Send Confirmation, Notify Dashboard.

#### [NEW] [workflow_6_voice_post_call.json](file:///d:/FlowZint/n8n/workflow_6_voice_post_call.json)
Processes the outcomes of inbound/outbound AI voice calls (WebSocket based) and routes follow-through actions accordingly.
- **Nodes**: Webhook (voice-call-complete), Switch on Call Outcome, Trigger Scheduler, Wait 2 Hours, Update Stage (closed_lost), Notify Dashboard.

---

## Verification Plan

### Manual Verification
1. Open the [n8n UI](https://n8n.io/).
2. Create a new workflow, click the top-right menu icon, and select **Import from File**.
3. Upload any of the generated JSON files from `d:\FlowZint\n8n\`.
4. Verify that all nodes render correctly, node parameters map correctly, and nodes are properly connected as described in the FlowZint n8n Implementation Guide.
