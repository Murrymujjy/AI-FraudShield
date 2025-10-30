# explain_agent.py
import os
import openai
import pandas as pd

# Load your API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_case(flagged_rows, clusters):
    """
    Use GPT model to explain suspicious transaction patterns.
    Fallback explanation will be provided if API is not available.
    """
    try:
        # Prepare context
        if isinstance(flagged_rows, pd.DataFrame):
            records = flagged_rows.head(10).to_dict(orient='records')
        elif isinstance(flagged_rows, list):
            records = flagged_rows[:10]
        else:
            records = []

        context_lines = [f"Flagged transactions (showing up to 10): {len(records)}"]
        for r in records:
            context_lines.append(
                f"- {r.get('tx_id', '?')} | {r.get('sender')} -> {r.get('receiver')} | "
                f"amount={r.get('amount')} | ts={r.get('timestamp')}"
            )

        context_lines.append(f"Detected clusters: {len(clusters)}")
        for c in clusters[:3]:
            context_lines.append(
                f"- Nodes: {', '.join(c['nodes'][:6])}... | Total moved: {c['total_moved']}"
            )

        prompt = (
            "\n".join(context_lines)
            + "\n\nExplain in plain English why these transactions appear suspicious. "
              "Then suggest 3 practical actions a bank compliance officer should take."
        )

        # If no key is found, fallback to local explanation
        if not openai.api_key:
            raise ValueError("Missing OpenAI API key")

        # Query GPT
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert fraud detection analyst."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
        )
        return resp["choices"][0]["message"]["content"]

    except Exception as e:
        # Fallback explanation (offline mode)
        return (
            f"LLM unavailable ({e}).\n"
            "Fallback explanation:\n"
            "Pattern shows rapid fund transfers from one sender to multiple receivers, "
            "often seen in money-mule or layering schemes. "
            "Recommended actions:\n"
            "1. Freeze suspicious accounts temporarily.\n"
            "2. Escalate for compliance review.\n"
            "3. Preserve logs and notify AML authorities if needed."
        )
