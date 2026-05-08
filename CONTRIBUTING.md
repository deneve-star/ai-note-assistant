# Contributing

Thanks for your interest in contributing to AI Note Assistant!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ai-note-assistant.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file (see README)

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## Code Style

We use [ruff](https://github.com/astral-sh/ruff) for linting:

```bash
pip install ruff
ruff check .
```

## Pull Requests

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run tests and linting
4. Submit a PR with a clear description

## Areas to Contribute

- New AI-powered features (semantic deduplication, note linking, etc.)
- Better test coverage
- Documentation improvements
- Performance optimizations for large note collections
