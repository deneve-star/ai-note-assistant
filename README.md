# AI Note Assistant

A simple CLI tool for managing and summarizing your notes with AI.

I built this because I was tired of having scattered notes everywhere and wanted a quick way to organize them and get summaries without opening heavy apps.

## Features

- Add, list, search and delete notes from the terminal
- Tag-based organization
- AI-powered note summarization (uses OpenAI-compatible APIs)
- Export notes to markdown
- SQLite storage — everything stays local

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

## Usage

```bash
# Add a note
python main.py add "Meeting notes: discussed roadmap for Q2" --tags work,meetings

# List all notes
python main.py list

# Search notes
python main.py search "roadmap"

# Summarize all notes (or by tag)
python main.py summarize
python main.py summarize --tag work

# Export to markdown
python main.py export notes_backup.md

# Delete a note by ID
python main.py delete 3
```

## How it works

Notes are stored in a local SQLite database. When you ask for a summary, the tool sends your notes to an AI model and returns a concise overview. Nothing fancy, just works.

## Tech stack

- Python 3.10+
- SQLite (via built-in `sqlite3`)
- `openai` library for AI calls
- `click` for CLI
- `python-dotenv` for config
