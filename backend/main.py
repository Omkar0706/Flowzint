from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import uuid

app = FastAPI()

# -------------------------------
# CORS
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# ROOT + HEALTH
# -------------------------------

@app.get("/")
async def home():
    return {"message": "FlowZint Backend Running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# -------------------------------
# INTERNAL EVENTS
# -------------------------------

@app.post("/internal/event")
async def internal_event(request: Request):
    data = await request.json()

    print("\n==============================")
    print("Received Internal Event")
    print("==============================")
    print(data)

    return {
        "status": "success",
        "received_data": data
    }

# -------------------------------
# LEAD QUALIFICATION AGENT
# -------------------------------

@app.post("/agents/qualify")
async def qualify_lead(request: Request):
    data = await request.json()

    print("\n==============================")
    print("Lead Qualification Request")
    print("==============================")
    print(data)

    message = data.get("message", "").lower()

    intent = "low"
    mood = "neutral"
    score = 40
    predicted_objection = "general"

    if "ai" in message or "automation" in message:
        intent = "high"
        mood = "excited"
        score = 85
        predicted_objection = "price"

    elif "demo" in message or "meeting" in message:
        intent = "high"
        mood = "interested"
        score = 90
        predicted_objection = "timing"

    elif "security" in message or "safe" in message:
        intent = "medium"
        mood = "curious"
        score = 70
        predicted_objection = "trust"

    return {
        "status": "qualified",
        "lead_id": data.get("lead_id"),
        "intent": intent,
        "mood": mood,
        "score": score,
        "predicted_objection": predicted_objection,
        "lead_data": data
    }

# -------------------------------
# OUTREACH GENERATION AGENT
# -------------------------------

@app.post("/agents/outreach")
async def generate_outreach(request: Request):
    data = await request.json()

    print("\n==============================")
    print("Outreach Generation Request")
    print("==============================")
    print(data)

    name = data.get("name", "Valued Client")
    company = data.get("company", "your company")
    email = data.get("email", "")
    intent = data.get("intent", "medium")

    if intent == "high":
        tone = "high-impact automation"
    else:
        tone = "workflow optimization"

    return {
        "status": "success",
        "email": email,
        "email_subject": f"How FlowZint can transform workflows at {company}",
        "email_body": f"""
        <html>
            <body>
                <p>Hi {name},</p>

                <p>
                Thank you for your interest in FlowZint.
                </p>

                <p>
                We help companies streamline operations using
                AI-driven workflow automation and intelligent agents.
                </p>

                <p>
                Based on your interest in high-impact automation,
                we'd love to schedule a quick call.
                </p>

                <p>
                Looking forward to speaking with you.
                </p>

                <br>

                <p>
                — Team FlowZint
                </p>
            </body>
        </html>
        """
    }

# -------------------------------
# NEGOTIATION AGENT
# -------------------------------

@app.post("/agents/negotiate")
async def negotiate(request: Request):
    data = await request.json()

    print("\n==============================")
    print("Negotiation Request")
    print("==============================")
    print(data)

    customer_message = data.get("customer_message", "").lower()

    objection = "general"

    if any(word in customer_message for word in ["price", "cost", "expensive"]):
        objection = "price"

    elif any(word in customer_message for word in ["time", "busy", "schedule"]):
        objection = "timing"

    elif any(word in customer_message for word in ["trust", "security", "safe"]):
        objection = "trust"

    elif any(word in customer_message for word in ["yes", "interested", "ok"]):
        objection = "interested"

    response_map = {
        "price": "We offer flexible pricing options and scalable plans based on your business size.",
        "timing": "No problem — we can schedule implementation according to your timeline.",
        "trust": "Security and reliability are core priorities for our platform.",
        "interested": "Fantastic! Let's move forward with scheduling a demo.",
        "general": "We'd love to understand your requirements better and help accordingly."
    }

    return {
        "status": "success",
        "response_message": response_map[objection],
        "detected_sentiment": "positive" if objection == "interested" else "neutral",
        "detected_objection_type": objection,
        "strategy_used": f"address-{objection}",
        "conversion_probability": 0.9 if objection == "interested" else 0.6
    }

# -------------------------------
# STALE LEADS API
# -------------------------------

@app.get("/api/leads/stale")
async def get_stale_leads():

    print("\nFetching stale leads...")

    return [
        {
            "id": "stale-lead-123",
            "name": "Jane Stale",
            "email": "jane@stalecompany.com",
            "company": "Stale Company",
            "updated_at": (
                datetime.utcnow() - timedelta(days=4)
            ).isoformat(),
            "days_since_contact": 4
        }
    ]

# -------------------------------
# FOLLOW-UP AGENT
# -------------------------------

@app.post("/agents/followup")
async def generate_followup(request: Request):
    data = await request.json()

    print("\n==============================")
    print("Follow-up Request")
    print("==============================")
    print(data)

    name = data.get("name", "Valued Client")

    return {
        "status": "success",
        "subject": "Still interested in FlowZint Automation?",
        "message": f"""
        <html>
            <body>
                <p>Hi {name},</p>

                <p>
                    We wanted to follow up and check whether you are still
                    exploring AI workflow automation solutions.
                </p>

                <p>
                    We'd be happy to show you how FlowZint can help.
                </p>

                <br>

                <p>
                    — Team FlowZint
                </p>
            </body>
        </html>
        """
    }

# -------------------------------
# SCHEDULER AGENT
# -------------------------------

@app.post("/agents/schedule")
async def schedule_meeting(request: Request):
    data = await request.json()

    print("\n==============================")
    print("Scheduler Request")
    print("==============================")
    print(data)

    now = datetime.utcnow()

    meeting_start = (
        now + timedelta(days=2)
    ).replace(
        hour=14,
        minute=0,
        second=0,
        microsecond=0
    )

    meeting_end = meeting_start + timedelta(minutes=30)

    return {
        "status": "success",
        "meeting_booked": True,
        "meeting_title": f"FlowZint Demo — {data.get('name', 'Client')}",
        "meeting_start": meeting_start.isoformat() + "Z",
        "meeting_end": meeting_end.isoformat() + "Z",
        "meeting_date": meeting_start.strftime("%B %d, %Y"),
        "meeting_time": meeting_start.strftime("%I:%M %p") + " UTC"
    }

# -------------------------------
# UPDATE LEAD STAGE
# -------------------------------

@app.patch("/api/leads/{lead_id}/stage")
async def update_lead_stage(lead_id: str, request: Request):

    data = await request.json()

    print("\n==============================")
    print(f"Updating Lead Stage: {lead_id}")
    print("==============================")
    print(data)

    return {
        "status": "success",
        "lead_id": lead_id,
        "stage": data.get("stage", "updated")
    }