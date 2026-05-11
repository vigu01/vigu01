# Teams Legal & Compliance Chat Agent (Google ADK)

A Microsoft Teams legal/compliance **chat agent** built with **Google ADK**.

It answers user questions using grounded evidence from:
- SharePoint (customer-managed access)
- Approved websites

## What this scaffold guarantees

1. **Customer-owned SharePoint access**
   - Each customer configures its own Entra app + permissions.
   - No tenant credentials are hardcoded.
2. **Grounded responses only**
   - Agent toolchain retrieves evidence first.
   - Final answer must include citations.
   - If evidence is missing, the agent declines and asks follow-up questions.
3. **Chat-agent design for Teams**
   - Exposes a chat-oriented `answer_question()` interface you can call from Teams handlers.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m src.main
```

## Environment variables

See `.env.example` for all settings.

## Production hardening checklist

- Replace demo retrievers with full Microsoft Graph + SharePoint integrations.
- Add persistent grounding storage (vector DB) and document freshness checks.
- Add enterprise auth, audit logs, policy logging, and PII redaction.
- Add Teams transport adapter and deployment packaging.
