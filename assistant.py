from openai import OpenAI
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL


def get_client() -> OpenAI:
    return OpenAI(api_key=AI_API_KEY, base_url=AI_BASE_URL)


def summarize_notes(notes: list[dict]) -> str:
    if not notes:
        return "No notes to summarize."

    if not AI_API_KEY:
        return "Error: AI_API_KEY not set. Add it to your .env file."

    notes_text = "\n".join(
        f"- [{n['created_at'][:10]}] {n['content']}" for n in notes
    )

    client = get_client()
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that summarizes personal notes. "
                    "Give a concise overview highlighting key themes and action items. "
                    "Keep it short and useful."
                ),
            },
            {
                "role": "user",
                "content": f"Summarize these notes:\n\n{notes_text}",
            },
        ],
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content
