# AI Note Assistant

A CLI tool for managing personal notes with AI-powered features: auto-tagging, semantic search, smart categorization, and multi-step analysis pipelines.

Built to solve the problem of scattered, unorganized notes — instead of manually tagging and searching, let AI handle the heavy lifting.

## Features

### Core
- Add, list, search, and delete notes from the terminal
- Tag-based organization
- Export notes to markdown
- SQLite storage — everything stays local

### AI-Powered
- **Auto-tagging** — AI analyzes note content and generates relevant tags automatically
- **Semantic search** — find notes by meaning, not just keywords (e.g., search "deadlines" finds notes about "due Friday")
- **Smart categorization** — AI groups notes by theme and highlights priorities
- **Multi-step analysis pipeline** — chain of AI calls: extract themes → identify action items → generate executive summary
- **Summarization** — get concise overviews of your note collection

## Setup

```bash
git clone https://github.com/deneve-star/ai-note-assistant.git
cd ai-note-assistant
pip install -r requirements.txt
```

Create a `.env` file with your API settings:

```env
AI_API_KEY=your-api-key-here
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```

Works with any OpenAI-compatible API (OpenAI, Mistral, Groq, local models via Ollama, etc.).

## Usage

```bash
# Add a note with manual tags
python main.py add "Meeting notes: discussed roadmap for Q2" --tags work,meetings

# Add a note with AI-generated tags
python main.py add "Deploy new API version by Friday" --auto-tag

# List all notes
python main.py list

# Filter by tag
python main.py list --tag work

# Keyword search
python main.py search "roadmap"

# AI semantic search (finds related notes even without exact keyword matches)
python main.py ai-search "upcoming deadlines"

# Summarize all notes
python main.py summarize

# Summarize by tag
python main.py summarize --tag work

# AI categorization (groups notes by theme)
python main.py categorize

# Full AI analysis pipeline (themes → actions → summary)
python main.py analyze

# Collection statistics
python main.py stats

# Export to markdown
python main.py export notes_backup.md

# Delete a note by ID
python main.py delete 3
```

## AI Analysis Pipeline

The `analyze` command runs a 3-step AI pipeline:

1. **Theme extraction** — identifies 3-5 main themes across all notes
2. **Action item detection** — finds tasks, deadlines, and commitments; prioritizes as HIGH/MEDIUM/LOW
3. **Executive summary** — combines themes and actions into a final report with "Next Steps"

This multi-step approach produces better results than a single prompt because each step builds context for the next one.

## Testing

```bash
pip install pytest
pytest tests/ -v
```

## Tech Stack

- Python 3.10+
- SQLite (via built-in `sqlite3`)
- `openai` library for AI calls (OpenAI-compatible)
- `click` for CLI
- `rich` for terminal formatting
- `python-dotenv` for config
- `pytest` for testing
- GitHub Actions for CI

## License

MIT
