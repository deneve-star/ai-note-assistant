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


def auto_tag(content: str) -> str:
    """Use AI to automatically generate relevant tags for a note."""
    if not AI_API_KEY:
        return ""

    client = get_client()
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a tagging assistant. Given a note, output 1-4 relevant tags "
                    "as a comma-separated list. Tags should be lowercase single words. "
                    "Only output the tags, nothing else. Example: work,meeting,urgent"
                ),
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        temperature=0.2,
        max_tokens=50,
    )

    raw = response.choices[0].message.content.strip()
    tags = [t.strip().lower() for t in raw.split(",") if t.strip()]
    return ",".join(tags[:4])


def smart_search(query: str, notes: list[dict]) -> list[dict]:
    """AI-powered semantic search -- finds relevant notes even without exact keyword matches."""
    if not notes or not AI_API_KEY:
        return []

    notes_block = "\n".join(
        f"[ID:{n['id']}] {n['content']}" for n in notes
    )

    client = get_client()
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a search assistant. Given a list of notes and a search query, "
                    "return ONLY the IDs of notes that are semantically relevant to the query. "
                    "Output comma-separated IDs, nothing else. If none match, output NONE."
                ),
            },
            {
                "role": "user",
                "content": f"Query: {query}\n\nNotes:\n{notes_block}",
            },
        ],
        temperature=0.1,
        max_tokens=100,
    )

    raw = response.choices[0].message.content.strip()
    if raw.upper() == "NONE":
        return []

    try:
        matched_ids = {int(x.strip()) for x in raw.split(",") if x.strip().isdigit()}
    except ValueError:
        return []

    return [n for n in notes if n["id"] in matched_ids]


def categorize_notes(notes: list[dict]) -> str:
    """Group notes by theme and highlight priorities using AI."""
    if not notes:
        return "No notes to categorize."

    if not AI_API_KEY:
        return "Error: AI_API_KEY not set. Add it to your .env file."

    notes_text = "\n".join(
        f"- [#{n['id']}, {n['created_at'][:10]}] {n['content']}" for n in notes
    )

    client = get_client()
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an organizational assistant. Analyze the notes and:\n"
                    "1. Group them into 2-5 thematic categories\n"
                    "2. For each category, list the note IDs that belong to it\n"
                    "3. Identify any action items or deadlines\n"
                    "4. Flag high-priority items\n"
                    "Format the output as a clean, readable report."
                ),
            },
            {
                "role": "user",
                "content": f"Categorize and analyze these notes:\n\n{notes_text}",
            },
        ],
        temperature=0.3,
        max_tokens=800,
    )

    return response.choices[0].message.content


def analyze_pipeline(notes: list[dict]) -> str:
    """Multi-step AI analysis: extract themes -> find action items -> generate report."""
    if not notes:
        return "No notes to analyze."

    if not AI_API_KEY:
        return "Error: AI_API_KEY not set. Add it to your .env file."

    notes_text = "\n".join(
        f"- [#{n['id']}, {n['created_at'][:10]}] {n['content']}" for n in notes
    )

    client = get_client()

    # Step 1: Extract key themes
    step1 = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract the 3-5 main themes from these notes. Output only the themes, one per line.",
            },
            {"role": "user", "content": notes_text},
        ],
        temperature=0.2,
        max_tokens=200,
    )
    themes = step1.choices[0].message.content

    # Step 2: Extract action items based on themes
    step2 = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Based on the themes and notes below, extract all action items, "
                    "deadlines, and commitments. Prioritize them as HIGH/MEDIUM/LOW."
                ),
            },
            {
                "role": "user",
                "content": f"Themes:\n{themes}\n\nNotes:\n{notes_text}",
            },
        ],
        temperature=0.2,
        max_tokens=400,
    )
    actions = step2.choices[0].message.content

    # Step 3: Generate final report
    step3 = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Create a final executive summary report combining the themes and "
                    "action items below. Make it concise but comprehensive. "
                    "Include a 'Next Steps' section at the end."
                ),
            },
            {
                "role": "user",
                "content": f"Themes:\n{themes}\n\nAction Items:\n{actions}",
            },
        ],
        temperature=0.3,
        max_tokens=600,
    )

    return (
        "=== AI Analysis Pipeline ===\n\n"
        f"-- Step 1: Key Themes --\n{themes}\n\n"
        f"-- Step 2: Action Items --\n{actions}\n\n"
        f"-- Step 3: Executive Summary --\n{step3.choices[0].message.content}"
    )
