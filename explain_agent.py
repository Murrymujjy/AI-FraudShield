# explain_agent.py
import os
try:
    import openai
except Exception:
    openai = None

openai_api_key = os.getenv('OPENAI_API_KEY')

def explain_case(flagged_rows, clusters):
    context_lines = []
    if isinstance(flagged_rows, list):
        fr = flagged_rows[:10]
    else:
        fr = flagged_rows.head(10).to_dict(orient='records')

    context_lines.append(f"Flagged transactions (showing up to 10): {len(fr)}")
    for r in fr:
        context_lines.append(f"- {r.get('tx_id')} | {r.get('sender')} -> {r.get('receiver')} | amount={r.get('amount')} | ts={r.get('timestamp')}")
    context_lines.append(f"Detected clusters: {len(clusters)}")
    for c in clusters[:3]:
        context_lines.append(f"- nodes: {c['nodes'][:6]}... total_moved={c['total_moved']}")

    prompt = "\n".join(context_lines) + "\n\nExplain why these look suspicious and suggest 3 actions for a bank compliance team.\n"

    if not openai_api_key or openai is None:
        return "OpenAI key not found or openai package unavailable. Fallback: rapid dispersal from one account to many accounts — likely money-mule network. Actions: freeze, investigate, preserve logs."
    openai.api_key = openai_api_key
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role':'system','content':'You are a helpful compliance analyst.'},
                      {'role':'user','content': prompt}],
            max_tokens=300
        )
        text = resp['choices'][0]['message']['content']
        return text
    except Exception as e:
        return f'LLM call failed: {e}\nFallback explanation: rapid dispersal pattern detected.'
