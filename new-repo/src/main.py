from bot import LegalComplianceChatAgent


def main() -> None:
    agent = LegalComplianceChatAgent()
    print(f"{agent.bot_name} is ready (Google ADK chat agent).")
    response = agent.answer_question("How are conflict-of-interest disclosures handled?")
    print("\nAnswer:\n")
    print(response["answer"])
    print("\nCitations:")
    for c in response["citations"]:
        print(f"- {c}")


if __name__ == "__main__":
    main()
