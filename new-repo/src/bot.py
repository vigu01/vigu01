from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Dict, Any

from google.adk.agents import Agent


@dataclass
class Evidence:
    source: str
    snippet: str


class GroundingError(RuntimeError):
    pass


class SharePointRetriever:
    """Customer-tenant SharePoint retrieval stub."""

    def search(self, query: str) -> List[Evidence]:
        return [
            Evidence(
                source="sharepoint://Legal/CodeOfConduct.docx",
                snippet="Employees must report conflicts of interest immediately.",
            )
        ]


class WebsiteRetriever:
    """Approved website retrieval stub."""

    def search(self, query: str) -> List[Evidence]:
        return [
            Evidence(
                source="https://compliance.example.com/conflicts-policy",
                snippet="Conflict disclosures are reviewed by Compliance within 5 business days.",
            )
        ]


class LegalComplianceChatAgent:
    def __init__(self) -> None:
        self.bot_name = os.getenv("BOT_NAME", "legal-compliance-agent")
        self.max_context_chunks = int(os.getenv("MAX_CONTEXT_CHUNKS", "8"))
        self.model = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")

        self.sharepoint = SharePointRetriever()
        self.websites = WebsiteRetriever()

        self.agent = Agent(
            name=self.bot_name,
            model=self.model,
            instruction=(
                "You are a legal and compliance chat agent for Microsoft Teams. "
                "Only answer from provided evidence. If evidence is missing or ambiguous, "
                "say you cannot answer yet and ask a clarifying question. Always include citations."
            ),
            tools=[self._retrieve_grounding_context],
        )

    def _retrieve_grounding_context(self, question: str) -> Dict[str, Any]:
        evidence = self.sharepoint.search(question) + self.websites.search(question)
        evidence = evidence[: self.max_context_chunks]

        if not evidence:
            raise GroundingError("No evidence found.")

        return {
            "question": question,
            "grounding": [
                {"source": item.source, "snippet": item.snippet} for item in evidence
            ],
        }

    def answer_question(self, question: str) -> Dict[str, Any]:
        try:
            context = self._retrieve_grounding_context(question)
        except GroundingError:
            return {
                "answer": (
                    "I don't have enough grounded legal/compliance evidence to answer yet. "
                    "Please share a narrower question or add approved sources."
                ),
                "citations": [],
                "grounded": False,
            }

        # NOTE: In production, call ADK runtime/session API to execute the agent with context.
        # Here we provide deterministic scaffold output while still using ADK Agent definition.
        citations = [item["source"] for item in context["grounding"]]
        answer = (
            "Based on grounded policy sources, employees must report conflicts of interest "
            "immediately, and Compliance reviews disclosures within 5 business days."
        )
        return {
            "answer": answer,
            "citations": citations,
            "grounded": True,
            "agent": self.agent.name,
            "model": self.model,
        }
