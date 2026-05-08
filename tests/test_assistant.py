import os
from unittest.mock import patch, MagicMock

os.environ.setdefault("DB_PATH", ":memory:")
os.environ.setdefault("AI_BASE_URL", "https://api.openai.com/v1")
os.environ.setdefault("AI_MODEL", "gpt-4o-mini")


SAMPLE_NOTES = [
    {"id": 1, "content": "Meeting with team about Q2 roadmap", "tags": "work,meeting", "created_at": "2025-01-15T10:00:00"},
    {"id": 2, "content": "Buy groceries: milk, eggs, bread", "tags": "personal", "created_at": "2025-01-16T12:00:00"},
    {"id": 3, "content": "Deploy new API version by Friday", "tags": "work,urgent", "created_at": "2025-01-17T09:00:00"},
]


class TestSummarizeNotes:
    def test_empty_notes(self):
        from assistant import summarize_notes
        assert summarize_notes([]) == "No notes to summarize."

    @patch("assistant.AI_API_KEY", "")
    def test_no_api_key(self):
        from assistant import summarize_notes
        result = summarize_notes(SAMPLE_NOTES)
        assert "AI_API_KEY" in result

    @patch("assistant.get_client")
    @patch("assistant.AI_API_KEY", "test-key")
    def test_successful_summary(self, mock_client):
        from assistant import summarize_notes
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Summary of notes"
        mock_client.return_value.chat.completions.create.return_value = mock_response
        result = summarize_notes(SAMPLE_NOTES)
        assert result == "Summary of notes"
        mock_client.return_value.chat.completions.create.assert_called_once()


class TestAutoTag:
    @patch("assistant.AI_API_KEY", "")
    def test_no_api_key(self):
        from assistant import auto_tag
        result = auto_tag("Some content")
        assert result == ""

    @patch("assistant.get_client")
    @patch("assistant.AI_API_KEY", "test-key")
    def test_successful_tagging(self, mock_client):
        from assistant import auto_tag
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "work,meeting,planning"
        mock_client.return_value.chat.completions.create.return_value = mock_response
        result = auto_tag("Meeting about project planning")
        assert "work" in result
        assert "meeting" in result


class TestSmartSearch:
    def test_empty_notes(self):
        from assistant import smart_search
        assert smart_search("query", []) == []

    @patch("assistant.AI_API_KEY", "")
    def test_no_api_key(self):
        from assistant import smart_search
        assert smart_search("query", SAMPLE_NOTES) == []

    @patch("assistant.get_client")
    @patch("assistant.AI_API_KEY", "test-key")
    def test_successful_search(self, mock_client):
        from assistant import smart_search
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "1,3"
        mock_client.return_value.chat.completions.create.return_value = mock_response
        results = smart_search("work tasks", SAMPLE_NOTES)
        assert len(results) == 2

    @patch("assistant.get_client")
    @patch("assistant.AI_API_KEY", "test-key")
    def test_search_no_matches(self, mock_client):
        from assistant import smart_search
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "NONE"
        mock_client.return_value.chat.completions.create.return_value = mock_response
        results = smart_search("something irrelevant", SAMPLE_NOTES)
        assert results == []


class TestCategorizeNotes:
    def test_empty_notes(self):
        from assistant import categorize_notes
        assert categorize_notes([]) == "No notes to categorize."

    @patch("assistant.AI_API_KEY", "")
    def test_no_api_key(self):
        from assistant import categorize_notes
        result = categorize_notes(SAMPLE_NOTES)
        assert "AI_API_KEY" in result

    @patch("assistant.get_client")
    @patch("assistant.AI_API_KEY", "test-key")
    def test_successful_categorize(self, mock_client):
        from assistant import categorize_notes
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Category 1: Work\n- #1, #3"
        mock_client.return_value.chat.completions.create.return_value = mock_response
        result = categorize_notes(SAMPLE_NOTES)
        assert "Category" in result


class TestAnalyzePipeline:
    def test_empty_notes(self):
        from assistant import analyze_pipeline
        assert analyze_pipeline([]) == "No notes to analyze."

    @patch("assistant.AI_API_KEY", "")
    def test_no_api_key(self):
        from assistant import analyze_pipeline
        result = analyze_pipeline(SAMPLE_NOTES)
        assert "AI_API_KEY" in result

    @patch("assistant.get_client")
    @patch("assistant.AI_API_KEY", "test-key")
    def test_successful_pipeline(self, mock_client):
        from assistant import analyze_pipeline
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Analysis result"
        mock_client.return_value.chat.completions.create.return_value = mock_response
        result = analyze_pipeline(SAMPLE_NOTES)
        assert "AI Analysis Pipeline" in result
        assert mock_client.return_value.chat.completions.create.call_count == 3
